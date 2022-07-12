import math
import random
import sys
from . import multi_fleet
from . import stars_math
from . import scan
from . import game_engine
from .cargo import Cargo, CARGO_TYPES
from .defaults import Defaults
from .location import Location
from .minerals import Minerals, MINERAL_TYPES
from .order import Order
from .reference import Reference
from .ship import Ship


""" Offset of ships from fleet center """
SHIP_OFFSET = stars_math.TERAMETER_2_LIGHTYEAR / 1000000000


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
    'ships': [], # ship references
    'under_construction': [], # BuShip references
    'order': Order(), # current actions
    'orders': [], # future actions
    'orders_repeat': False,
    'fuel_reserve': (30, 0, 100), # minimum fuel reserve before cross-fleet sharing
}

""" Temporary values (default, min, max)  """
__tmp_defaults = {
    'player': Reference('Player'),
    'stats': None,
    'location': None,
    'cargo': None,
    'fuel': None,
    'initiative': None,
    'move_to': None,
    'is_stationary': True,
    'order_complete': True,
    'hyperdenial_effect': [0.0, 0.0],
    'hyperdenial_players': [],
}

""" Class defining fleets - directly modifiable by the player """
class Fleet(Defaults):
    """ Initialize and register """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)

    """ Provide calculated values """
    def __getattribute__(self, name):
        self_dict = object.__getattribute__(self, '__dict__')
        # Safety check if inital defaults have not been applied or if has value
        if '__init_complete__' not in self_dict or name not in self_dict or (self_dict[name] is not None and name != 'location'):
            return super().__getattribute__(name)
        # Calculate if not yet calculated
        if name == 'stats':
            self_dict[name] = Ship(from_ships=self.ships)
        elif name == 'location':
            if len(self.ships) > 0:
                self_dict[name] = self.ships[0].location
            else:
                self_dict[name] = Location()
        elif name == 'cargo':
            self_dict[name] = Cargo()
            for s in self.ships:
                self_dict[name] += s.cargo
        elif name == 'fuel':
            self_dict[name] = 0
            for s in self.ships:
                self_dict[name] += s.fuel
        elif name == 'initiative':
            self_dict[name] = max(self.ships, key=lambda x: x.initiative).initiative
        return super().__getattribute__(name)

    """ Adds ships to the fleet """
    def __add__(self, ships):
        return self.add_ships(ships)

    """ Adds ships to the fleet """
    def add_ships(self, ships):
        if isinstance(ships, Fleet):
            all_ships = ships.ships
            all_ships += ships.under_construction
            ships = all_ships
        elif not isinstance(ships, list):
            ships = [ships]
        for ship in ships:
            ship = Reference(ship)
            if ship ^ 'Ship' and ship not in self.ships:
                self.ships.append(ship)
            if ship ^ 'BuShips' and ship not in self.under_construction:
                self.under_construction.append(ship)
        self.stats = None
        self.cargo = None
        self.fuel = None
        self.initiative = None
        return self

    """ Remove ship from fleet """
    def __sub__(self, ships):
        return self.remove_ships(ships)

    """ Remove ship from fleet """
    def remove_ships(self, ships):
        if isinstance(ships, Fleet):
            ships = ships.ships
        elif not isinstance(ships, list):
            ships = [ships]
        for ship in ships:
            if ship in self.ships:
                self.ships.remove(ship)
            elif ship in self.under_construction:
                self.under_construction.remove(ship)
        # Remove from player fleets and let die
        if len(self.ships) == 0 and len(self.under_construction) == 0:
            if self in self.player.fleets:
                self.player.fleets.remove(self)
        self.stats = None
        self.cargo = None
        self.fuel = None
        self.initiative = None
        return self

    """ Duplicates the flees except for the ships for use with split """
    def duplicate(self):
        f = Fleet()
        f.order = Order(self.order)
        for o in self.orders:
            f.orders.append(Order(o))
        f.orders_repeat = self.orders_repeat
        f.fuel_reserve = self.fuel_reserve
        return f

    """ Update cache """
    def next_hundreth(self):
        self.move_to = self.location
        self.is_stationary = True
        self.order_complete = True
        self.hyperdenial_effect = [0.0, 0.0]
        self.hyperdenial_players = []

    """ Update location and apply orbit offset """
    def update_location(self, location):
        # Either offset from ship 0 or orbit the thing being referenced
        offset = 10
        reference = location.reference
        if not reference:
            if len(self.ships) > 0:
                reference = Reference(self.ships[0])
        else:
            # Distance in km from the point or heavenly body being centerd on
            offset_distances = {'Sun': 7000, 'Planet': 7000}
            offset = offset_distances.get(+(location.reference), offset)
        # Update all ships
        for s in self.ships:
            if reference == s:
                s.location = Location(location)
            else:
                s.location = Location(reference=reference, offset=offset * stars_math.KILOMETER_2_LIGHTYEAR)
        self.location = location

    """ Check if the fleet can/ordered to move """
    def read_orders(self):
        # Fleets with ships under construction cannot move
        if len(self.under_construction) > 0:
            multi_fleet.add(self)
            return
        # Space stations cannot move, ships with no engines cannot move
        for ship in self.ships:
            if ship.is_space_station():
                multi_fleet.add(self)
                return
            elif len(ship.engines) == 0:
                multi_fleet.add(self)
                return
        self.move_to = self.order.move_calc(self.location)
        #print(self.move_to.__dict__)
        if self.move_to.root_location != self.location.root_location:
            self.is_stationary = False

    """ Colonize planets per the order """
    def colonize(self):
        # No people, no colonizing
        if not self.stats.is_colonizer or self.cargo.people == 0:
            return
        # Filter the fleet for colonizers and then sort by age
        colonizers = []
        for ship in self.ships:
            if ship.is_colonizer and ship.cargo.people > 0:
                colonizers.append(ship)
        colonizers.sort(key=lambda x: x.commissioning, reverse=True)
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
        # Colonize
        for p in planets:
            if len(colonizers) == 0:
                return
            if p.colonize(self.player):
                p.on_surface += colonizers[-1].cargo
                colonizers[-1].scrap()
                self -= colonizers.pop()

    """ Deploy hyperdenial """
    def activate_hyperdenial(self):
        # Not scheduled to move
        if self.is_stationary:
            self.stats.hyperdenial.activate(self.player, self.location.root_location)

    """ Hyperdenials affecting me """
    def in_hyperdenial(self, effect, other_player, blackhole=False):
        if blackhole:
            self.hyperdenial_effect[1] += effect
        else:
            self.hyperdenial_effect[0] += effect
        # Players that will have visibility of fleet if fleet moves
        if other_player and other_player not in self.hyperdenial_players:
            self.hyperdenial_players.append(other_player)

    """ Does all the moving calculations and then moves the ships """
    def move(self):
        if self.is_stationary:
            return
        print('\n * Fleet Move Is Called', end=' $ ')
        # Determine speed
        speed = self.order.speed
        hyperdenial = self.hyperdenial_effect
        stop_at = None
        distance = 0.0
        # Manual stargate or auto stargate
        start, end = self._stargate_find(allow_damage=(speed == -2))
        if (speed == -2 or speed == -1) and (start and end):
            # TODO pay for stargateing
            stop_at = end.location
            distance = self.location - stop_at
            for ship in self.ships:
                ship.gate(distance, start.stats.stargate.strength)
        # Manual stargate but no gate or ship would be destroyed
        elif speed == -2:
            pass
        # Auto speed
        elif speed == -1:
            # initial speed
            distance = self.location - self.move_to
            if distance < 1:
                speed = math.ceil(math.sqrt(distance * 100.0))
            else:
                speed = 10
                distance = 1
            # reduce speed until safe
            while speed > 0:
                stop_at = self.location.move(self.move_to, distance)
                if self._fuel_calc(speed, distance, hyperdenial) <= self.fuel and self._damage_check(speed, hyperdenial) == 0:
                    break
                speed -= 1
                distance = (speed ** 2) / 100
        # Manual speed
        else:
            distance = min(self.location - self.move_to, (speed ** 2) / 100)
            stop_at = self.location.move(self.move_to, distance)
            if self._fuel_calc(speed, distance, hyperdenial) > self.fuel:
                speed = 1
                distance = min(self.location - self.move_to, (speed ** 2) / 100)
                stop_at = self.location.move(self.move_to, distance)
        # Move the fleet
        if stop_at:
            print('Fleet:', self.ID, 'Moved', end=' : ')
            print('origonal position:', self.location.xyz, end=' -> ')
            self.update_location(stop_at)
            print('new location', self.location.xyz)
            # Moved in a hyperdenial field
            scan.hyperdenial(self, self.hyperdenial_players)
            # Blackhole message
            if hyperdenial[1] > 0.0:
                pass #TODO blackhole message
        if distance <= 0.0:
            self.is_stationary - True
        else:
            # Use fuel
            self.fuel -= self._fuel_calc(speed, distance, hyperdenial)
            # Apply any over-drive damage and siphon antimatter
            for ship in self.ships:
                mass_per_engine = ship['mass_per_engine']
                for engine in ship.engines:
                    self.fuel += engine.siphon_calc(distance)
                    ship.take_damage(0, engine.damage_calc(speed, mass_per_engine, distance, hyperdenial))
            self.fuel_distribution() # Do now in case of ships dying in battle
        if self.location.root_location != self.move_to.root_location:
            self.order_complete = False
        multi_fleet.add(self)

    """ Post combat, move inside the system """
    def move_in_system(self):
        if self.move_to.root_location == self.location.root_location:
            self.update_location(self.move_to)

    """ Orbital mineral extraction """
    def orbital_extraction(self):
        if not self.is_stationary or self.stats.extraction_rate == 0 or not self.location.reference ^ 'Planet' or self.location.reference.is_colonized():
            return
        for ship in self.ships:
            for (component, qty) in ship.components.items():
                if component.extraction_rate > 0:
                    cargo_space = self.stats.cargo_max - self.cargo.sum()
                    self.cargo += self.location.reference.extract_minerals(component, qty, cargo_space)
        # cargo is intentionally not redistributed yet

    """ Lay mines """
    def lay_mines(self):
        if not self.is_stationary or self.stats.mines_laid == 0 or not self.location.in_system:
            return
        self.location.root_reference.lay_mines(int(self.stats.mines_laid / 100), self.player)

    """ Check that there is a planet that is colonized by someone other than you, then tell all ships that can bomb to bomb it """
    def bomb(self):
        if not self.is_stationary or len(self.stats.bombs) == 0 or not self.location.reference ^ 'Planet' or not self.location.reference.is_colonized():
            return
        planet = self.location.reference
        if self.player.get_relation(planet.player) != 'enemy':
            return
        for b in self.stats.bombs:
            planet.bomb(b)

    """ Steal from other players """
    def piracy(self):
        if not self.is_stationary or not (self.stats.is_piracy_cargo or self.stats.is_piracy_fuel):
            return
        enemy = []
        neutral = []
        for f in multi_fleet.get(self.location):
            relation = self.player.get_relation(f.player)
            if relation == 'enemy':
                enemy.append(f)
            elif relation == 'neutral':
                neutral.append(f)
        # Pirate enemies first
        random.shuffle(enemy)
        random.shuffle(neutral)
        for mark in enemy + neutral:
            cargo_space = self.stats.cargo_max - self.cargo.sum()
            if self.stats.is_piracy_cargo and cargo_space > 0:
                for m in MINERAL_TYPES:
                    steal = min(mark.cargo[m], cargo_space)
                    self.cargo[m] += steal
                    mark.cargo[m] -= steal
                    cargo_space -= steal
            fuel_space = self.stats.fuel_max - self.fuel
            if self.stats.is_piracy_fuel and fuel_space > 0:
                steal = min(mark.fuel, fuel_space)
                self.fuel += steal
                mark.fuel -= steal

    """ Unload cargo """
    def unload(self):
        if not self.is_stationary:
            return
        (cargo, cargo_max) = self._other_cargo()
        if not cargo or cargo.sum() >= cargo_max:
            return
        order = {'titanium': max(0, -1*self.order.load_ti), 'lithium': max(0, -1*self.order.load_li), 'silicon': max(0, -1*self.order.load_si), 'people': max(0, -1*self.order.load_pop)} # cannot use cargo type because of 0 min
        # TODO check unloading people on non-owned planet
        for ctype in CARGO_TYPES:
            if order[ctype] > 0:
                order[ctype] = min(cargo_max - cargo.sum(), order[ctype], self.cargo[ctype])
                self.cargo[ctype] -= order[ctype]
                cargo[ctype] += order[ctype]
        for ctype in CARGO_TYPES:
            if order[ctype] == -1:
                order[ctype] = min(cargo_max - cargo.sum(), self.cargo[ctype])
                self.cargo[ctype] -= order[ctype]
                cargo[ctype] += order[ctype]
        # cargo is intentionally not redistributed yet

    """ Conduct trade """
    def buy(self):
        if not self.is_stationary:
            return
        #TODO

    """ Scrap """
    def scrap(self):
        if not self.is_stationary or not self.order.scrap:
            return
        if self.cargo.people > 0:
            if self.location.reference ^ 'Planet' and self.location.reference.player == self.player:
                self.location.reference.on_surface.people += self.cargo.people
            else:
                #TODO error message
                # Cancel scrap order
                self.order.scrap = False
                return
        for s in self.ships:
            s.scrap()
        self - self.ships

    """ Load cargo """
    def load(self):
        if not self.is_stationary:
            return
        (cargo, cargo_max) = self._other_cargo()
        if not cargo or self.cargo.sum() >= self.stats.cargo_max:
            return
        order = {'titanium': self.order.load_ti, 'lithium': self.order.load_li, 'silicon': self.order.load_si, 'people': self.order.load_people} # cannot use cargo type because of 0 min
        # TODO check loading people on non-owned planet
        for ctype in CARGO_TYPES:
            if order[ctype] > 0:
                order[ctype] = min(self.stats.cargo_max - self.cargo.sum(), order[ctype], cargo[ctype])
                cargo[ctype] -= order[ctype]
                self.cargo[ctype] += order[ctype]
        for ctype in CARGO_TYPES:
            if order[ctype] == -1:
                order[ctype] = min(self.stats.cargo_max - self.cargo.sum(), cargo[ctype])
                cargo[ctype] -= order[ctype]
                self.cargo[ctype] += order[ctype]
        # cargo is intentionally not redistributed yet

    """ Transfers ownership of the fleet to the specified player """
    def transfer(self):
        if not self.order.transfer_to:
            return
        if len(self.under_construction):
            return
        if self.cargo.people > 0:
            # TODO message
            return
        self.order.transfer_to.add_ships(self.ships)
        self.player.remove_ships(self)

    """ Merges the fleet with the target fleet """
    def merge(self): # TODO Test
        f = self.location.reference
        if not self.order.merge or not f ^ 'Fleet' or f != self.order.location.reference or f.player != self.player:
            return
        ~f + self.ships
        ~f + self.under_construction
        self.player.remove_ships(self)
    
    """ Perform anticloak scanning """
    def scan_anticloak(self):
        if self.stats.scanner.anti_cloak > 0:
            scan.anticloak(self.player, self.location, self.stats.scanner.anti_cloak)

    """ Perform hyperdenial scanning """
    def scan_hyperdenial(self):
        if self.stats.hyperdenial.radius > 0:
            scan.hyperdenial(self.player, self.location, self.stats.hyperdenial.radius)
           
    """ Perform penetrating scanning """
    def scan_penetrating(self):
        if self.stats.scanner.penetrating > 0:
            scan.penetrating(self.player, self.location, self.stats.scanner.penetrating)

    """ Perform normal scanning """
    def scan_normal(self):
        if self.stats.scanner.normal > 0:
            scan.normal(self.player, self.location, self.stats.scanner.normal)

    """ Create a report about itself """
    def scan_self(self):
        for ship in self.ships:
            self.player.add_intel(self, ship.scan_report('self'))

    """ find the stargates to use """
    def _stargate_find(self, allow_damage):
        distance = self.move_to - self.location
        gate_needed = max(self.ships, key=lambda x: x.total_mass).total_mass + distance
        start_gates = []
        end_gates = []
        # Find stargates that allow transit
        for fleet in multi_fleet.get(self.location):
            if fleet.stats.stargate.strength > 0:
                cost = self.player.get_treaty(fleet.player).buy_gate
                if cost >= 0:
                    start_gates.append((max(0, gate_needed - fleet.stats.stargate.strength), cost, len(start_gates), fleet))
        # Find stargates that allow transit
        for fleet in multi_fleet.get(self.move_to):
            if fleet.stats.stargate.strength > 0:
                cost = self.player.get_treaty(fleet.player).buy_gate
                if cost >= 0 or self.player.race.primary_race_trait == 'Patryns':
                    end_gates.append((0, cost, len(end_gates), fleet))
        if len(start_gates) == 0 or len(end_gates) == 0:
            return (None, None)
        start_gates.sort()
        end_gates.sort()
        if start_gates[0][0] > 0:
            # Don't gate if trying to avoid damage
            if not allow_damage:
                return (None, None)
            # Don't gate if a ship will definitely die
            for ship in self.ships:
                if not ship.gate(distance, start_gates[0][3].stats.stargate.strength, survival_test=True):
                    return (None, None)
        return (start_gates[0][3], end_gates[0][3])

    """ Cargo of unload/load fleet/planet """
    def _other_cargo(self):
        if self.location.reference ^ 'Fleet':
            if self.location.reference.player == self.player:
                return (self.location.reference.cargo, self.location.reference.stats.cargo_max)
        elif self.location.reference ^ 'Planet' or self.location.reference ^ 'Sun':
            if self.location.reference.player == self.player:
                return (self.location.reference.on_surface, sys.maxsize)
        return (None, 0)

    """ Calculates fuel usage for fleet """
    def _fuel_calc(self, speed, distance, denials):
        fuel = 0
        for ship in self.ships:
            mass_per_engine = ship['mass_per_engine']
            for engine in ship.engines:
                fuel += engine.fuel_calc(speed, mass_per_engine, distance, denials)
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
        if self.stats.fuel_max > 0 and self.fuel > 0:
            fuel_left = self.fuel
            for ship in self.ships:
                ship.fuel = int(self.fuel * ship.fuel_max / self.stats.fuel_max)
                fuel_left -= ship.fuel
            for ship in self.ships:
                while fuel_left > 0 and ship.fuel < ship.fuel_max:
                    ship.fuel += 1
                    fuel_left -= 1
        else:
            self.fuel = 0
            for ship in self.ships:
                ship.fuel = 0
    
    """ Evenly distributes the cargo back to the ships """
    def cargo_distribution(self):
        if self.stats.cargo_max == 0.0:
            return
        cargo_left = Cargo(self.cargo)
        for ctype in CARGO_TYPES:
            for ship in self.ships:
                ship.cargo[ctype] = int(self.cargo[ctype] * ship.cargo_max / self.stats.cargo_max)
                cargo_left[ctype] -= ship.cargo[ctype]
        for ctype in CARGO_TYPES:
            for ship in self.ships:
                while cargo_left[ctype] > 0 and ship.cargo.sum() < ship.cargo_max:
                    ship.cargo[ctype] += 1
                    cargo_left[ctype] -= 1
        for ship in self.ships:
            ship.update_cargo()

Fleet.set_defaults(Fleet, __defaults, __tmp_defaults)

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
''' """ Tiernan's with more senceical codeing: """
    """ evenly distributed protection, mines fill in the gap latter not while the ships are still there """
        mines = system.mines
        sweep = 0
        attract = 0
        for ship in self.ships:
            sweep += ship.sweep_mines(mines)
            attract += ship.attract_mines(mines)
        attack = max(0, attract - sweep)
        system.sweep(sweep)
        for ship in self.ships:
            ship.hit_mines(round(attack), system)
'''
