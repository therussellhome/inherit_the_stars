import math
import sys
import copy
from . import multi_fleet
from . import stars_math
from . import scan
from . import game_engine
from . import hyperdenial
from .cargo import Cargo, CARGO_TYPES
from .defaults import Defaults
from .location import Location
from .order import Order
from .location import Location
from .reference import Reference
from .tech import Tech


""" Offset of ships from fleet center """
SHIP_OFFSET = stars_math.TERAMETER_2_LIGHTYEAR / 1000000000


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
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
                if ship.location.xyz == self.location.xyz or ship.location.reference_root == self.location.reference_root:
                    ship.location = Location(reference=self, offset=SHIP_OFFSET)
                    self.ships.append(ship)
                else:
                    print('Cannot add ship to fleet - not at the same location', self.location, ship.location, file=sys.stderr)
        self._stats(fleet_change=True)
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
        if len(self.ships) == 0:
            pass #TODO remove from player's fleets
        self._stats(fleet_change=True)
        return self

    """ Check if the fleet can/ordered to move """
    def move_calc(self):
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

    """ Deploy hyperdenial """
    def hyperdenial(self):
        # Not scheduled to move
        if self._stats().hyperdenial.radius > 0 and self.__cache__['move'] == None:
            for ship in self.ships:
                ship.hyperdenial.activate(ship.player)

    """ Does all the moving calculations and then moves the ships """
    def move(self):
        # Calculate destination (patrol, standoff, etc)
        move = self.__cache__['move']
        if move == None:
            self.__cache__['moved'] = False
            multi_fleet.add(self)
            return
        # Determine speed
        stats = self._stats()
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
        self._fuel_distribution(stats.fuel)

    """ Post combat, move inside the system """
    def move_in_system(self):
        in_system = self.__cache__['move_in_system']
        if in_system != None and in_system.reference_root == self.location.reference_root:
            self.location = in_system

    """ Repair only self if moving, else repair most damaged fleet here """
    def repair(self):
        if self.__cache__['moved']:
            self.apply_repair(self._stats().repair_moving)
        else:
            # TODO apply to the most damaged friendly fleet at this location
            self.apply_repair(self._stats().repair)

    """ How damaged is the fleet """
    def damage_level(self):
        damage = 0
        for ship in self.ships:
            damage += ship.armor_damage
        return damage / self._stats().armor

    """ Apply repair to this fleet """
    def apply_repair(self, repair_points):
        ships = self.ships[:]
        for i in range(repair_points):
            ships.sort(key=lambda x: x.armor_damage / x.armor, reverse=True)
            ships[0].armor_damage -= 1

    """ Orbital mineral extraction """
    def orbital_extraction(self):
        stats = self._stats()
        if self.__cache__['moved'] or stats.orbital_extraction == 0:
            return
        




    """ Update cached values of the fleet """
    def _stats(self, fleet_change=False):
        if 'stats' not in self.__cache__ and fleet_change:
            # Skip the computational effort if cache not yet needed
            return
        elif 'stats' not in self.__cache__ or fleet_change:
            stats = Tech()
            self.__cache__['stats'] = stats
            stats.init_from(self.ships)
            stats.__dict__['repair_moving'] = 0
            for ship in self.ships:
                stats['repair_moving'] += ship.hull.repair
                ship.update_cache()
            return stats
        return self.__cache__['stats']

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
    def _fuel_distribution(self, fuel):
        stats = self._stats()
        if stats.fuel_max > 0 and fuel > 0:
            stats.fuel = fuel
            fuel_left = fuel
            for ship in self.ships:
                ship.fuel = int(fuel * ship.fuel_max / stats.fuel_max)
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
    def _cargo_distribution(self, cargo):
        stats = self._stats()
        stats.cargo = cargo
        cargo_left = copy.copy(cargo)
        for ctype in CARGO_TYPES:
            for ship in self.ships:
                ship.cargo[ctype] = int(cargo[ctype] * ship.cargo_max / stats.cargo_max)
                cargo_left[ctype] -= ship.cargo[ctype]
        for ctype in CARGO_TYPES:
            for ship in self.ships:
                while cargo_left[ctype] > 0 and ship.cargo.sum() < ship.cargo_max:
                    ship.cargo[ctype] += 1
                    cargo_left[ctype] -= 1
    
           

    """ Merges the fleet with the target fleet """
    def merge(self, player):
        o_fleet = self.waypoints[0].recipiants['merge']
        if type(o_fleet) != type(Fleet()) or o_fleet not in player.fleets:
            return
        for ship in self.ships:
            o_fleet.ships.append(ship)
        player.remove_fleet(self)
    
    """ Splits the fleet as specified in the waypoint orders """
    def split(self, player):
        for split in self.waypoints[0].splits:
            player.create_fleet(ships = split, waypoints = copy.copy(self.waypoints))
            for ship in split:
                self.ships.remove(ship)
        if len(self.ships) == 0:
            player.remove_fleet(self)
    
    """ Transfers ownership of the fleet to the specified player """
    def transfer(self, player):
        if self.cargo.people > 0:
            return
        player_2 = self.waypoints[0].recipiants['transfer']
        self.waypoints = [self.waypoints[0]]
        player_2.add_fleet(self)
        if self in player_2.fleets:
            player.remove_fleet(self)
    
    """ Executes the unload function """
    def unload(self, player):
        recipiant = self.waypoints[0].recipiants['unload']
        if not self.check_self(recipiant, player) and recipiant.is_colonized():
            return
        """ gets the fuel and cargo from your ships """
        self_cargo, self_cargo_max = self.get_cargo()
        self_fuel, self_fuel_max = self.get_fuel()
        if recipiant in player.fleets:
            """ gets fuel and cargo from the ships in the other fleet """
            load_cargo, load_cargo_max = recipiant.get_cargo()
            load_fuel, load_fuel_max = recipiant.get_fuel()
        else:
            """ ensures cargo is correctly fetched from the planet's surface and fuel is fetched from the space stations fuel tanks """
            load_cargo = recipiant.on_surface
            load_cargo_max = recipiant.on_surface.cargo_max
            load_fuel, load_fuel_max = recipiant.space_stations.get_fuel()
        """ checks if the amount of each sceduled transhipment of cargo or fuel is fullfilable and ajusts the amount if not """
        for transfer in self.waypoints[0].transfers['unload']:
            item = transfer[0]
            amount = transfer[1]
            amount = self.handle_cargo(self_fuel, load_fuel, load_fuel_max, item, amount, load_cargo, load_cargo_max, self_cargo)
            """ actual transhipment of cargo and fuel """
            if item == 'fuel':
                load_fuel += amount
                self_fuel -= amount
            else:
                load_cargo[item] += amount
                self_cargo[item] -= amount
        """ returns the fuel and cargo to your ships """
        for item in ["titanium", "silicon", "lithium", "people"]:
            self.distribute_cargo(self_cargo, item, self_cargo_max)
        self.distribute_fuel(self_fuel, self_fuel_max)
        if recipiant in player.fleets:
            """ returns fuel and cargo to the ships in the other fleet """
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.distribute_cargo(load_cargo, item, load_cargo_max)
            recipiant.distribute_fuel(load_fuel, load_fuel_max)
        else:
            """ ensures cargo is correctly stoed on the planet's surface and fuel is in the space stations fuel tanks """
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.on_surface[item] = load_cargo[item]
            recipiant.space_stations.distribute_fuel(load_fuel, load_fuel_max)
    
    """ Executes the sell function """
    def sell(self, player):
        recipiant = self.waypoints[0].recipiants['sell']
        if not self.check_trade(recipiant, player):
            return
        """ gets the fuel and cargo from your ships """
        self_cargo, self_cargo_max = self.get_cargo()
        self_fuel, self_fuel_max = self.get_fuel()
        if False:#TODO recipiant.__class__.__name__ == 'fleet':
            """ gets fuel and cargo from the ships in the other fleet """
            load_cargo, load_cargo_max = recipiant.get_cargo()
            load_fuel, load_fuel_max = recipiant.get_fuel()
        else:
            """ ensures cargo is correctly fetched from the planet's surface and fuel is fetched from the space stations fuel tanks """
            load_cargo = recipiant.on_surface
            load_cargo_max = recipiant.on_surface.cargo_max
            load_fuel, load_fuel_max = recipiant.space_stations.get_fuel()
        """ checks if the amount of each sceduled purchase of cargo or fuel is fullfilable at price and ajusts the amount if not """
        for transfer in self.waypoints[0].transfers['sell']:
            item = transfer[0]
            amount = transfer[1]
            traety = player.get_treaty(recipiant.player)
            abreve = False
            if item == 'fuel':
                abreve = item
            if item in ['titanium', 'silicon', 'lithium']:
                abreve = item[0:2]
            if abreve and traety['sell_' + abreve] >= 0:
                amount = self.handle_cargo(self_fuel, load_fuel, load_fuel_max, item, amount, load_cargo, load_cargo_max, self_cargo)
                true_amount = int(recipiant.player.spend('trade', traety['sell_' + abreve] * amount, False) / traety['sell_' + abreve])
                """ actual purchace of cargo and fuel,  """
                if item == 'fuel':
                    load_fuel += true_amount
                    self_fuel -= true_amount
                else:
                    load_cargo[item] += true_amount
                    self_cargo[item] -= true_amount
                player.energy += recipiant.player.spend('trade', traety['sell_' + abreve] * true_amount)
        """ returns the fuel and cargo to your ships """
        for item in ["titanium", "silicon", "lithium", "people"]:
            self.distribute_cargo(self_cargo, item, self_cargo_max)
        self.distribute_fuel(self_fuel, self_fuel_max)
        if False:#TODO recipiant.__class__.__name__ == 'fleet':
            """ returns fuel and cargo to the ships in the other fleet """
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.distribute_cargo(load_cargo, item, load_cargo_max)
            recipiant.distribute_fuel(load_fuel, load_fuel_max)
        else:
            """ ensures cargo is correctly stoed on the planet's surface and fuel is in the space stations fuel tanks """
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.on_surface[item] = load_cargo[item]
            recipiant.space_stations.distribute_fuel(load_fuel, load_fuel_max)
    
    """ Generic method for handling cargo """
    def handle_cargo(self, unload_fuel, load_fuel, load_fuel_max, item, amount, load_cargo, load_cargo_max, unload_cargo):
        print(amount, item, 'with problem', end=' ')
        if item in ["fuel", "titanium", "silicon", "lithium", "people"]:
            if item == 'fuel':
                if unload_fuel < amount and (load_fuel_max - load_fuel) >= unload_fuel:
                    print("'not enough", item + "'", "{'fuel':", str(unload_fuel) + "}", end=' ')
                    amount = unload_fuel
                elif (load_fuel_max - load_fuel) < amount and unload_fuel >= (load_fuel_max - load_fuel):
                    print("'not enough capacity'", "{'fuel':", str(load_fuel_max) + ", 'fuel_max':", str(load_fuel_max) + "}", end=' ')
                    amount = (load_fuel_max - load_fuel)
                else:
                    print('none ', end='')
            else:
                if unload_cargo[item] < amount and (load_cargo_max - load_cargo._sum()) >= unload_cargo[item]:
                    print("'not enough", item + "'", unload_cargo.__dict__, end=' ')
                    amount = unload_cargo[item]
                elif (load_cargo_max - load_cargo._sum()) < amount and unload_cargo[item] >= (load_cargo_max - load_cargo._sum()):
                    print("'not enough capacity'", load_cargo.__dict__, "'cargo_max':", load_cargo_max, end=' ')
                    amount = (load_cargo_max - load_cargo._sum())
                else:
                    print('none ', end='')
        print('becomes', amount)
        return amount
    
    """ Executes the buy function """
    def buy(self, player):
        recipiant = self.waypoints[0].recipiants['buy']
        if not self.check_trade(recipiant, player):
            return
        """ gets the fuel and cargo from your ships """
        self_cargo, self_cargo_max = self.get_cargo()
        self_fuel, self_fuel_max = self.get_fuel()
        if False:#TODO recipiant.__class__.__name__ == 'fleet':
            """ gets fuel and cargo from the ships in the other fleet """
            unload_cargo, unload_cargo_max = recipiant.get_cargo()
            unload_fuel, unload_fuel_max = recipiant.get_fuel()
        else:
            """ ensures cargo is correctly fetched from the planet's surface and fuel is fetched from the space stations fuel tanks """
            unload_cargo = recipiant.on_surface
            unload_fuel, unload_fuel_max = recipiant.space_stations.get_fuel()
        """ checks if the amount of each sceduled purchace of cargo or fuel is fullfilable at price and ajusts the amount if not """
        for transfer in self.waypoints[0].transfers['buy']:
            item = transfer[0]
            amount = transfer[1]
            traety = player.get_treaty(recipiant.player)
            if item == 'fuel':
                abreve = item
            if item in ['titanium', 'silicon', 'lithium']:
                abreve = item[0:2]
            if traety['buy_' + abreve] >= 0:
                amount = self.handle_cargo(unload_fuel, self_fuel, self_fuel_max, item, amount, self_cargo, self_cargo_max, unload_cargo)
                true_amount = int(player.spend('trade', traety['buy_' + abreve] * amount, False) / traety['buy_' + abreve])
                """ actual purchace of cargo and fuel """
                if item == 'fuel':
                    unload_fuel -= true_amount
                    self_fuel += true_amount
                else:
                    unload_cargo[item] -= true_amount
                    self_cargo[item] += true_amount
                recipiant.player.energy += player.spend('trade', traety['buy_' + abreve] * true_amount)
        """ returns the fuel and cargo to your ships """
        for item in ["titanium", "silicon", "lithium", "people"]:
            self.distribute_cargo(self_cargo, item, self_cargo_max)
        self.distribute_fuel(self_fuel, self_fuel_max)
        if False:#TODO recipiant.__class__.__name__ == 'fleet':
            """ returns fuel and cargo to the ships in the other fleet """
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.distribute_cargo(unload_cargo, item, unload_cargo_max)
            recipiant.distribute_fuel(unload_fuel, unload_fuel_max)
        else:
            """ ensures cargo is correctly stoed on the planet's surface and fuel is in the space stations fuel tanks """
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.on_surface[item] = unload_cargo[item]
            recipiant.space_stations.distribute_fuel(unload_fuel, unload_fuel_max)
        
    """ Eelles the first ship in the fleet that can colonize to colonize the planet specified in the waypoint orders """
    def colonize(self, player):
        planet = self.waypoints[0].recipiants['colonize']
        if planet not in game_engine.get('Planet'):
            return
        if planet.is_colonized():
            return
        for ship in self.ships:
            if ship.colonizer and ship.cargo.people > 0:
                ship.colonize(Reference(player), planet)
                ship.scrap(planet, self.location)
                self.ships.remove(ship)
                if len(self.ships) == 0:
                    player.remove_fleet(self)
                break
    
    """ Scraps all the ships in the fleet """
    def scrap(self):
        planet = self.waypoints[0].recipiants['scrap']
        for ship in self.ships:
            ship.scrap(planet, self.location)
    
    """ A check to ensure you do not give away or steal minerals or people from a planet or fleet that is not yours """
    def check_self(self, recipiant, player):
        if recipiant in player.fleets:
            print('Fleet-Yours')
            return True
        if recipiant in game_engine.get('Planet'):
            print('Planet-', end='')
            if recipiant.is_colonized() and recipiant.player.ID != player.ID:
                print('Other')
                return False
            print('Yours or Uninhadited')
            print(recipiant.player.ID)
            print(player.ID)
            return True
        return False
    
    """ Checks that you are not enemies and might trade """
    def check_trade(self, recipiant, player):
        if recipiant in game_engine.get('Planet'):
            print(player.get_treaty(recipiant.player).status)
            if player.get_treaty(recipiant.player).relation != 'enemy' and player.get_treaty(recipiant.player).is_active():
                return True
        return False
    
    """ Executes the load function """
    def load(self, player):
        recipiant = self.waypoints[0].recipiants['load']
        if not self.check_self(recipiant, player):
            return
        """ gets the fuel and cargo from your ships """
        self_cargo, self_cargo_max = self.get_cargo()
        self_fuel, self_fuel_max = self.get_fuel()
        if recipiant in player.fleets:
            """ gets fuel and cargo from the ships in the other fleet """
            unload_cargo, unload_cargo_max = recipiant.get_cargo()
            unload_fuel, unload_fuel_max = recipiant.get_fuel()
        else:
            """ ensures cargo is correctly fetched from the planet's surface and fuel is fetched from the space stations fuel tanks """
            unload_cargo = recipiant.on_surface
            unload_fuel, unload_fuel_max = recipiant.space_stations.get_fuel()
        """ checks if the amount of each sceduled transhipment of cargo or fuel is fullfilable and ajusts the amount if not """
        for transfer in self.waypoints[0].transfers['load']:
            item = transfer[0]
            amount = transfer[1]
            amount = self.handle_cargo(unload_fuel, self_fuel, self_fuel_max, item, amount, self_cargo, self_cargo_max, unload_cargo)
            """ actual transhipment of cargo and fuel """
            if item == 'fuel':
                unload_fuel -= amount
                self_fuel +=  amount
            else:
                unload_cargo[item] -= amount
                self_cargo[item] += amount
        """ returns the fuel and cargo to your ships """
        for item in ["titanium", "silicon", "lithium", "people"]:
            self.distribute_cargo(self_cargo, item, self_cargo_max)
        self.distribute_fuel(self_fuel, self_fuel_max)
        if recipiant in player.fleets:
            """ returns fuel and cargo to the ships in the other fleet """
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.distribute_cargo(unload_cargo, item, unload_cargo_max)
            recipiant.distribute_fuel(unload_fuel, unload_fuel_max)
        else:
            """ ensures cargo is correctly stoed on the planet's surface and fuel is in the space stations fuel tanks """
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.on_surface[item] = unload_cargo[item]
            recipiant.space_stations.distribute_fuel(unload_fuel, unload_fuel_max)
    
    """ Repairs ships, prioitizing your fleet and then your other fleets before other friendly units """
    def repair_friendlys(self, player):
        repair_points = 0
        ships_here = {'self':{'ships':[], 'damage':0}, 'you':{'ships':[], 'damage':0}, 'friendly':{'ships':[], 'damage':0}}
        for ship in self.ships:
            repair_points += ship.open_repair_bays() + ship.damage_control()
            ships_here['self']['ships'].append(ship)
            ships_here['self']['damage'] += ship.max_armor() - ship.armor
        for fleet in player.fleets:
            if (self.location - fleet.location) == 0 and fleet != self:
                for ship in fleet.ships:
                    ships_here['you']['ships'].append(ship)
                    ships_here['you']['damage'] += ship.max_armor() - ship.armor
        #TODO Repair bays enable repair of ships, belonging to other players, that are at the same location.  
        #for ship in find_bin(self.location):
        #    if ship.PlayerID != player.ID and get_player(ship.PlayerID).get_treaty(player).relation == 'team':
        #        if (self.location - ship.location) == 0:
        #            ships_here['friendly']['ships'].append(ship)
        #            ships_here['friendly']['damage'] += ship.max_armor() - ship.armor
        repair_points = self.distribute_repair(ships_here['self'], repair_points)
        repair_points = self.distribute_repair(ships_here['you'], repair_points)
        repair_points = self.distribute_repair(ships_here['friendly'], repair_points)
    
    """ Tells the ships to repair """
    def distribute_repair(self, ships_here, repair_points):
        repair_points_left = repair_points
        damage = ships_here['damage']
        damage_fixed = 0
        temp_repair = min(repair_points, damage)
        for ship in ships_here['ships']:
            amount = int(temp_repair * ((ship.max_armor() - ship.armor) / damage) * (temp_repair / damage))
            ship.repair_self(amount)
            repair_points_left -= amount
            damage_fixed += amount
        for ship in ships_here['ships']:
            if temp_repair > damage_fixed:
                ship.repair_self(1)
                damage_fixed += 1
                repair_points_left -= 1
        ships_here['damage'] -= damage_fixed
        return repair_points_left
    
    """ Tells any ships that can lay mines to lay mines """
    def lay_mines(self, player):
        system = self.waypoints[0].recipiants['lay_mines']
        for ship in self.ships:
            ship.lay_mines(player, system)
    
    """ Tells all the ships to repair themselves (damage_control) """
    def repair_ship(self):
        if 'repair' in self.waypoints[0].actions:
            return
        for ship in self.ships:
            repair_self(ship.damage_control())
    
    """ Tells all the ships that can conduct orbital mining to conduct orbital mining as detailed in their waypoint orders """
    def orbital_mining(self):
        planet = self.waypoints[0].recipiants['orbital_mining']
        if planet not in game_engine.get('Planet'):
            return False
        for ship in self.ships:
            ship.orbital_mining(planet)
    
    """ UNWRITEN """
    def patrol(self, player):
        pass #TODO
    
    """ UNWRITEN """
    def piracy(self, player):
        pass #TODO
    
    """ Check that there is a planet that is colonized by someone other than you, then tell all ships that can bomb to bomb it """
    def bomb(self, player):
        planet = self.waypoints[0].recipiants['bomb']
        #print("player.get_treaty(planet.player).__dict__ :\n", player.get_treaty(planet.player).__dict__)
        print("player.get_treaty(planet.player).relation == 'enemy'", player.get_treaty(planet.player).relation == 'enemy')
        if planet in game_engine.get('Planet') and planet.is_colonized() and planet.player != player and player.get_treaty(planet.player).relation == 'enemy':
            shields = planet.raise_shields()
            pop = planet.on_surface.people
            facility_kill = 0
            pop_kill = 0
            #print(planet.facilities['defenses'].quantity, pop, self.ships[0].bombs[0].percent_defense(pop, shields))
            for ship in self.ships:
                f_kill, p_kill = ship.bomb(planet, shields, pop)
                facility_kill += f_kill
                pop_kill += p_kill
            planet.facilities['defenses'].quantity -= round(facility_kill)
            planet.on_surface.people -= round(pop_kill)
            #print(planet.on_surface.people)

    """ Perform anticloak scanning """
    def scan_anticloak(self):
        anticloak = 0
        for ship in self.ships:
            anticloak = max(anticloak, ship.scanner.anti_cloak)
        if anticloak > 0:
            scan.anticloak(ships[0].player, fleet.location, anticloak)

    """ Perform hyperdenial scanning """
    def scan_hyperdenial(self):
        hyperdenial = 0
        for ship in self.ships:
            hyperdenial = max(hyperdenial, ship.hyperdenial.range)
        if hyperdenial > 0:
            scan.hyperdenial(ships[0].player, fleet.location, hyperdenial)
           
    """ Perform penetrating scanning """
    def scan_penetrating(self):
        penetrating = 0
        for ship in self.ships:
            penetrating = max(penetrating, ship.scanner.penetrating)
        if penetrating > 0:
            scan.penetrating(ships[0].player, fleet.location, penetrating)

    """ Perform normal scanning """
    def scan_normal(self):
        normal = 0
        for ship in self.ships:
            normal = max(normal, ship.scanner.normal)
        if normal > 0:
            scan.normal(ships[0].player, fleet.location, normal)

    """ Sum field across ships """
    def _sum(self, field, total=0):
        for ship in ships:
            total += ship[field]
        return total

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
