import copy
import math
import random
import sys
from . import multi_fleet
from . import stars_math
from . import scan
from . import game_engine
from . import hyperdenial
from .cargo import Cargo, CARGO_TYPES
from .defaults import Defaults
from .location import Location
from .minerals import Minerals, MINERAL_TYPES
from .order import Order
from .location import Location
from .reference import Reference
from .ship import Ship


""" Offset of ships from fleet center """
SHIP_OFFSET = stars_math.TERAMETER_2_LIGHTYEAR / 1000000000


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
    'player': Reference('Player'),
    'order': Order(), # current actions
    'orders': [], # future actions
    'orders_repeat': False,
    'ships': [],
    'location': Location(),
}


""" Class defining fleets - directly modifiable by the player """
class Fleet(Defaults):
    """ Initialize the cache """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__cache__['order_complete'] = True
        self.__cache__['move'] = None
        self.__cache__['move_in_system'] = None
        self.__cache__['moved'] = False
        game_engine.register(self)

    """ Adds ships to the fleet and correct location """
    def __add__(self, ships):
        if isinstance(ships, Fleet):
            ships = ships.ships
        elif not isinstance(ships, list):
            ships = [ships]
        for ship in ships:
            if ship not in self.ships:
                if ship.location.xyz == self.location.xyz or ship.location.root_location == self.location.root_location:
                    ship.location = Location(reference=self, offset=SHIP_OFFSET)
                    self.ships.append(ship)
                else:
                    print('Cannot add ship to fleet - not at the same location', self.location, ship.location, file=sys.stderr)
        if 'stats' in self.__cache__:
            del self.__cache__['stats']
        return self

    """ Remove ship from fleet """
    def __sub__(self, ships):
        if isinstance(ships, Fleet):
            ships = ships.ships
        elif not isinstance(ships, list):
            ships = [ships]
        for ship in ships:
            if ship in self.ships:
                self.ships.remove(ship)
        # Remove from player fleets and let die
        if len(self.ships) == 0:
            if self in self.player.fleets:
                self.player.fleets.remove(self)
        if 'stats' in self.__cache__:
            del self.__cache__['stats']
        return self

    """ Duplicates the flees except for the ships for use with split """
    def duplicate(self):
        f = Fleet()
        f.order = copy.copy(self.order)
        for o in self.orders:
            f.orders.append(copy.copy(o))
        f.orders_repeat = self.orders_repeat
        f.location = copy.copy(self.location)
        return f

    """ Update cache """
    def next_hundreth(self):
        if 'stats' in self.__cache__:
            del self.__cache__['stats']

    """ Check if the fleet can/ordered to move """
    def read_orders(self):
        self.__cache__['move'] = None
        # Set move in system in case combat displaces
        self.__cache__['move_in_system'] = self.location
        # Space stations cannot move, ships with no engines cannot move
        for ship in self.ships:
            if ship.is_space_station():
                return
            elif len(ship.engines) == 0:
                return
        (self.__cache__['move'], self.__cache__['move_in_system']) = self.order.move_calc(self.location)

    """ Colonize planets per the order """
    def colonize(self):
        stats = self.stats()
        if not stats.is_colonizer or stats.cargo.people == 0:
            return
        # Check for planets meeting the criteria
        planets = []
        if self.location.in_system:
            max_terraform = self.player.max_terraform()
            hab_terraform = (max_terraform, max_terraform, max_terraform)
            for planet in self.location.root_reference.planets:
                if planet.is_colonized():
                    continue
                elif self.order.colonize_manual:
                    if self.order.location.reference and self.order.location.reference == planet:
                        planets.append(planet)
                elif planet.habitability(self.player.race, hab_terraform) >= self.order.colonize_min_hab:
                    min_minerals = Minerals(titanium=self.order.colonize_min_ti, lithium=self.order.colonize_min_li, silicon=self.order.colonize_min_si)
                    if planet.mineral_availability() >= min_minerals:
                        planets.append(planet)
        if len(planets) == 0:
            return
        planets.sort(key=lambda x: x.habitability(self.player.race), reverse=True)
        # Filter the fleet for colonizers and then sort by age
        colonizers = []
        for ship in self.ships:
            if ship.is_colonizer and ship.cargo.people > 0:
                colonizers.append(ship)
        colonizers.sort(key=lambda x: x.commissioning, reverse=True)
        # Colonize
        for p in planets:
            if len(colonizers) == 0:
                return
            if p.colonize(self.player):
                p.on_surface += colonizers[-1].cargo
                p.on_surface += colonizers[-1].scrap_value()
                self -= colonizers.pop()

    """ Deploy hyperdenial """
    def hyperdenial(self):
        # Not scheduled to move
        if self.stats().hyperdenial.radius > 0 and self.__cache__['move'] == None:
            for ship in self.ships:
                ship.hyperdenial.activate(self.player)

    """ Does all the moving calculations and then moves the ships """
    def move(self):
        # Calculate destination (patrol, standoff, etc)
        move = self.__cache__['move']
        if move == None:
            self.__cache__['moved'] = False
            multi_fleet.add(self)
            return
        # Determine speed
        stats = self.stats()
        speed = self.order.speed
        # Manual stargate or auto stargate
        if speed == -2 or (speed == -1 and self._stargate_check()):
            self.__cache__['moved'] = False
            # stargate use allows fleet actions this hundredth
            self.__cache__['move_in_system'] = move
            #TODO stargates
            multi_fleet.add(self)
            return
        # Auto speed
        elif speed == -1:
            # initial speed
            distance = self.location - move
            if distance < 1:
                speed = math.ceil(math.sqrt(distance * 100.0))
            else:
                speed = 10
                distance = 1
            # reduce speed until safe
            while speed > 0:
                stop_at = self.location.move(move, distance)
                denials = hyperdenial.transit(self.location, stop_at)
                print(speed, distance, stop_at.xyz)
                if self._fuel_calc(speed, denials, distance) <= stats.fuel and self._damage_check(speed, denials) == 0:
                    break
                speed -= 1
                distance = (speed ** 2) / 100
        # Manual speed
        else:
            distance = min(self.location - move, (speed ** 2) / 100)
            stop_at = self.location.move(move, distance)
            denials = hyperdenial.transit(self.location, stop_at)
            if self._fuel_calc(speed, distance, denials) > stats.fuel:
                speed = 1
                distance = min(self.location - move, (speed ** 2) / 100)
                stop_at = self.location.move(move, distance)
                denials = hyperdenial.transit(self.location, stop_at)
        # Move the fleet
        self.location = self.location.move(move, distance)
        if self.location != self.__cache__['move']:
            self.__cache__['order_complete'] = False
        self.__cache__['moved'] = True
        multi_fleet.add(self)
        # Use fuel
        stats.fuel -= self._fuel_calc(speed, denials, distance)
        # Apply any over-drive damage and siphon antimatter
        for ship in self.ships:
            mass_per_engine = ship['mass_per_engine']
            for engine in ship.engines:
                stats.fuel += engine.siphon_calc(distance)
                ship.take_damage(0, engine.damage_calc(speed, mass_per_engine, denials, distance))
        self.fuel_distribution() # Do now in case of ships dying in battle

    """ Post combat, move inside the system """
    def move_in_system(self):
        in_system = self.__cache__['move_in_system']
        if in_system != None and in_system.root_location == self.location.root_location:
            self.location = in_system

    """ Repair only self if moving, else repair most damaged fleet here """
    def repair(self):
        if self.__cache__['moved']:
            self.apply_repair(self.stats().repair_moving)
        else:
            # TODO apply to the most damaged friendly fleet at this location
            self.apply_repair(self.stats().repair)

    """ How damaged is the fleet """
    def damage_level(self):
        damage = 0
        for ship in self.ships:
            damage += ship.armor_damage
        return damage / self.stats().armor

    """ Apply repair to this fleet """
    def apply_repair(self, repair_points):
        ships = self.ships[:]
        for i in range(repair_points):
            ships.sort(key=lambda x: x.armor_damage / x.armor, reverse=True)
            ships[0].armor_damage -= 1

    """ Orbital mineral extraction """
    def orbital_extraction(self):
        stats = self.stats()
        if self.__cache__['moved'] or stats.extraction_rate == 0 or not self.location.reference ^ 'Planet' or self.location.reference.is_colonized():
            return
        for ship in self.ships:
            for (component, qty) in ship.components.items():
                if component.extraction_rate > 0:
                    cargo_space = stats.cargo_max - stats.cargo.sum()
                    stats.cargo += self.location.reference.extract_minerals(component, qty, cargo_space)
        # cargo is intentionally not redistributed yet

    """ Lay mines """
    def lay_mines(self):
        stats = self.stats()
        if self.__cache__['moved'] or stats.mines_laid == 0 or not self.location.in_system:
            return
        self.location.root_reference.lay_mines(int(stats.mines_laid / 100), self.player)

    """ Check that there is a planet that is colonized by someone other than you, then tell all ships that can bomb to bomb it """
    def bomb(self):
        stats = self.stats()
        if self.__cache__['moved'] or len(stats.bombs) == 0 or not self.location.reference ^ 'Planet' or not self.location.reference.is_colonized():
            return
        planet = self.location.reference
        if self.player.get_relation(planet.player) != 'enemy':
            return
        for b in stats.bombs:
            planet.bomb(b)

    """ Steal from other players """
    def piracy(self):
        stats = self.stats()
        if self.__cache__['moved'] or not (stats.is_piracy_cargo or stats.is_piracy_fuel):
            return
        marks = []
        for f in multi_fleet.get(self.location):
            if self.player.get_relation(f.player) not in ['me', 'team']:
                marks.append(f)
        random.shuffle(marks)
        for mark in marks:
            mstats = mark.stats()
            cargo_space = stats.cargo_max - stats.cargo.sum()
            if stats.is_piracy_cargo and cargo_space > 0:
                for m in MINERAL_TYPES:
                    steal = min(mstats.cargo[m], cargo_space)
                    stats.cargo[m] += steal
                    mstats.cargo[m] -= steal
                    cargo_space -= steal
            fuel_space = stats.fuel_max - stats.fuel
            if stats.is_piracy_fuel and fuel_space > 0:
                steal = min(mstats.fuel, fuel_space)
                stats.fuel += steal
                mstats.fuel -= steal

    """ Unload cargo """
    def unload(self):
        if self.__cache__['moved']:
            return
        stats = self.stats()
        (cargo, cargo_max) = self._other_cargo()
        if not cargo or cargo.sum() >= cargo_max:
            return
        order = {'titanium': self.order.unload_ti, 'lithium': self.order.unload_li, 'silicon': self.order.unload_si, 'people': self.order.unload_people} # cannot use cargo type because of 0 min
        # TODO check unloading people on non-owned planet
        for ctype in CARGO_TYPES:
            if order[ctype] > 0:
                order[ctype] = min(cargo_max - cargo.sum(), order[ctype], stats.cargo[ctype])
                stats.cargo[ctype] -= order[ctype]
                cargo[ctype] += order[ctype]
        for ctype in CARGO_TYPES:
            if order[ctype] == -1:
                order[ctype] = min(cargo_max - cargo.sum(), stats.cargo[ctype])
                stats.cargo[ctype] -= order[ctype]
                cargo[ctype] += order[ctype]
        # cargo is intentionally not redistributed yet

    """ Conduct trade """
    def buy(self):
        if self.__cache__['moved']:
            return
        #TODO

    """ Scrap """
    def scrap(self):
        if self.__cache__['moved'] or not self.order.scrap:
            return
        stats = self.stats()
        if self.location.reference ^ 'Planet' and stats.cargo.people > 0:
            if self.location.reference.player == self.player:
                self.location.reference.on_surface.people += stats.cargo.people
            else:
                #TODO error message
                # Cancel scrap order
                self.order.scrap = False
                return
        stats.scrap()

    """ Load cargo """
    def load(self):
        if self.__cache__['moved']:
            return
        stats = self.stats()
        (cargo, cargo_max) = self._other_cargo()
        if not cargo or stats.cargo.sum() >= stats.cargo_max:
            return
        order = {'titanium': self.order.load_ti, 'lithium': self.order.load_li, 'silicon': self.order.load_si, 'people': self.order.load_people} # cannot use cargo type because of 0 min
        # TODO check loading people on non-owned planet
        for ctype in CARGO_TYPES:
            if order[ctype] > 0:
                order[ctype] = min(stats.cargo_max - stats.cargo.sum(), order[ctype], cargo[ctype])
                cargo[ctype] -= order[ctype]
                stats.cargo[ctype] += order[ctype]
        for ctype in CARGO_TYPES:
            if order[ctype] == -1:
                order[ctype] = min(stats.cargo_max - stats.cargo.sum(), cargo[ctype])
                cargo[ctype] -= order[ctype]
                stats.cargo[ctype] += order[ctype]
        # cargo is intentionally not redistributed yet

    """ Transfers ownership of the fleet to the specified player """
    def transfer(self):
        if not self.order.transfer_to:
            return
        if self.stats().cargo.people > 0:
            # TODO message
            return
        self.player.remove_fleet(self)
        self.player = self.order.transfer_to
        self.player.add_fleet(self)
        self.orders = []
        self.orders_repeat = False

    """ Merges the fleet with the target fleet """
    def merge(self):
        f = self.location.reference
        if not f ^ 'Fleet' or f.player != self.player:
            return
        for ship in self.ships:
            f += ship
        self.player.remove_fleet(self)
    
    """ Perform anticloak scanning """
    def scan_anticloak(self):
        stats = self.stats()
        if stats.scanner.anti_cloak > 0:
            scan.anticloak(self.player, self.location, stats.scanner.anti_cloak)

    """ Perform hyperdenial scanning """
    def scan_hyperdenial(self):
        stats = self.stats()
        if stats.hyperdenial.radius > 0:
            scan.hyperdenial(self.player, self.location, stats.hyperdenial.radius)
           
    """ Perform penetrating scanning """
    def scan_penetrating(self):
        stats = self.stats()
        if stats.scanner.penetrating > 0:
            scan.penetrating(self.player, self.location, stats.scanner.penetrating)

    """ Perform normal scanning """
    def scan_normal(self):
        stats = self.stats()
        if stats.scanner.normal > 0:
            scan.normal(self.player, self.location, stats.scanner.normal)

    """ Update cached values of the fleet """
    def stats(self):
        if 'stats' not in self.__cache__:
            stats = Ship(from_ships=self.ships)
            self.__cache__['stats'] = stats
            stats.__dict__['repair_moving'] = 0
            stats.scanner.anti_cloak = 0
            stats.hyperdenial.radius = 0
            stats.scanner.penetrating = 0
            stats.scanner.normal = 0
            stats.initiative = 0
            stats.location = self.location
            for ship in self.ships:
                ship.update_cache(self.player)
                stats['repair_moving'] += ship.hull.repair
                stats.scanner.anti_cloak = max(stats.scanner.anti_cloak, ship.scanner.anti_cloak)
                stats.hyperdenial.radius = max(stats.hyperdenial.radius, ship.hyperdenial.radius)
                stats.scanner.penetrating = max(stats.scanner.penetrating, ship.scanner.penetrating)
                stats.scanner.normal = max(stats.scanner.normal, ship.scanner.normal)
                if ship['initiative'] > stats.initiative:
                    stats.initiative = ship['initiative']
            return stats
        return self.__cache__['stats']

    """ Cargo of unload/load fleet/planet """
    def _other_cargo(self):
        stats = self.stats()
        if self.location.reference ^ 'Fleet':
            if self.location.reference.player == self.player:
                otherstats = self.location.reference.stats()
                return (otherstats.cargo, otherstats.cargo_max)
        elif self.location.reference ^ 'Planet' or self.location.reference ^ 'Sun':
            if self.location.reference.player == self.player:
                return (self.location.reference.on_surface, sys.maxsize)
        return (None, 0)

    """ Check if fleet can safely gate to waypoint """
    def _stargate_check(self):
        return False #TODO

    """ Calculates fuel usage for fleet """
    def _fuel_calc(self, speed, denials, distance):
        fuel = 0
        for ship in self.ships:
            mass_per_engine = ship['mass_per_engine']
            for engine in ship.engines:
                fuel += engine.fuel_calc(speed, mass_per_engine, denials, distance)
        return fuel
        
    """ Checks if you can safely move at a certain speed with your entire fleet """
    def _damage_check(self, speed, denials):
        for ship in self.ships:
            mass_per_engine = ship['mass_per_engine']
            for engine in ship.engines:
                if engine.tachometer(speed, mass_per_engine, denials) > 100:
                    return True
        return False
    
    """ Evenly distributes the fuel between the ships """
    def fuel_distribution(self):
        stats = self.stats()
        if stats.fuel_max > 0 and stats.fuel > 0:
            fuel_left = stats.fuel
            for ship in self.ships:
                ship.fuel = int(stats.fuel * ship.fuel_max / stats.fuel_max)
                fuel_left -= ship.fuel
            for ship in self.ships:
                while fuel_left > 0 and ship.fuel < ship.fuel_max:
                    ship.fuel += 1
                    fuel_left -= 1
        else:
            stats.fuel = 0
            for ship in self.ships:
                ship.fuel = 0
    
    """ Evenly distributes the cargo back to the ships """
    def cargo_distribution(self):
        stats = self.stats()
        cargo_left = copy.copy(stats.cargo)
        for ctype in CARGO_TYPES:
            for ship in self.ships:
                ship.cargo[ctype] = int(stats.cargo[ctype] * ship.cargo_max / stats.cargo_max)
                cargo_left[ctype] -= ship.cargo[ctype]
        for ctype in CARGO_TYPES:
            for ship in self.ships:
                while cargo_left[ctype] > 0 and ship.cargo.sum() < ship.cargo_max:
                    ship.cargo[ctype] += 1
                    cargo_left[ctype] -= 1

Fleet.set_defaults(Fleet, __defaults)

""" In-system movment mine interaction """
''' Aryon:
    """ protect self first then help other ships """
        mines = system.mines
        track = []
        for i in range(len(self.ships)):
            sweep = self.ships[i].sweep_mines(mines)
            attract = self.ships[i].attract_mines(mines)
            track.append([sweep-attract, copy.copy(sweep), attract, self.ships[i]])
        track.sort(reverse = True)
        sweep = 0
        for tracked in track:
            sweep += tracked[1] 
            sweep, attack = max(0, sweep - tracked[2]), max(0, tracked[2] - sweep)
            system.sweep(tracked[2]-attack)
            tracked[3].hit_mines(attack, system)
        system.sweep(sweep)
'''
''' Tiernan:
    """ evenly distributed protection """
        mines = system.mines
        sweep = 0
        attract = 0
        for ship in self.ships:
            sweep += ship.sweep_mines(mines)
            attract += ship.attract_mines(mines)
        system.sweep(sweep)
        attack = max(0, attract - sweep)/attract
        for ship in self.ships:
            ship.hit_mines(round(ship.attract_mines(mines) * attack), system)
'''
