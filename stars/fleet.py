import sys
import copy
from . import stars_math
from . import scan
from . import game_engine
from .cargo import Cargo
from .defaults import Defaults
from .location import Location
from .waypoint import Waypoint
from .location import Location
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'waypoints': [],
    'fuel': (0, 0, sys.maxsize),
    'fuel_max': (0, 0, sys.maxsize),
    'ships': [],
    'cargo': Cargo(),
    'location': Location(),
}


""" Class defining fleets - directly modifiable by the player """
class Fleet(Defaults):
    """ Adds ships to the fleet and  """
    def add_ships(self, ships):
        for ship in ships:
            if len(self.ships) == 0:
                self.location = copy.copy(ship.location)
                self.ships.append(ship)
            else:
                if (self.location - ship.location) <= (stars_math.TERAMETER_2_LIGHTYEAR * 2) and ship not in self.ships:
                    self.ships.append(ship)

    """ Remove ship from fleet """
    def remove_ship(self, ship):
        if ship in self.ships:
            self.ships.remove(ship)
        if len(self.ships) == 0:
            pass #TODO remove from player's fleets
    
    #""" checks if can upgrade and then stops moving if comanded to """
    #def check_upgrade(self, player):
    #    if self.waypoints[1].upgrade_if_commanded == True and self.waypoints[1].location in game_engine.get('Planets/') and self.waypoints[1].location.space_station:
    #        for ship in self.ships:
    #            if ship.new_design and ship.new_design.mass <= self.waypoints[1].location.space_station.max_build_mass:
    #                self.waypoints[1].location.upgrade(ship)
    
    """ Does all the moving calculations and then moves the ships """
    def move(self, player):
        if len(self.waypoints) < 2:
            return
        self.waypoints[1].move_to(self)
        num_denials = 0
        fuel, fleet_fuel_max = self.get_fuel()
        #""" finds how many hyper denial fields the fleet is passing through """
        #for hyper_denial in game_engine.hyper_denials:
        #    distance_to_denial = self.location - hyper_denial.location
        #    if distance_to_denial >= hyper_denial.range and hyper_denial.player.treaties[player.name].relation == 'enemy':
        #        num_denials += 1
        speed = self.waypoints[1].speed
        mode = self.waypoints[1].mode
        distance_to_waypoint = self.location - self.waypoints[1].fly_to
        distance_at_hyper = (speed**2)/100
        """ ensures the fleet goes as far as it can, either all the way to the waypoint or maximum distance it can go at it's hyper level """
        if distance_to_waypoint < distance_at_hyper:
            distance = distance_to_waypoint
        else:
            distance = distance_at_hyper
        if self.waypoints[1].depart == 'after x years':
            self.waypoints[1].years -= 0.01
        repair_check = 0
        if self.waypoints[1].depart == 'repair to x':
            for ship in self.ships:
                repair_check += ship.max_armor() / ship.armor * 100
            repair_check /= len(self.ships)
        if distance_to_waypoint == 0:
            if self.waypoints[1].depart == 'immediately' or self.waypoints[1].depart == 'after x years' and self.waypoint[1].years == 0 or self.waypoints[1].depart == 'repair to x' and self.waypoints[1].repair_to <= repair_check:
                self.waypoints.pop(0)
                self.move(player)
            else:
                return
        """ checks to ensure the ships can actualy move, have the fuel to move, and won't be damaged """
        if self.test_damage(speed, num_denials) == None:
            return
        if mode == "auto":
            while self.test_fuel(speed, num_denials, distance, fuel) or self.test_damage(speed, num_denials) != False:
                if self.test_damage(speed, num_denials) == None:
                    return
                speed -= 1
                distance_at_hyper = (speed**2)/100
                if distance_to_waypoint < distance_at_hyper:
                    distance = distance_to_waypoint
                else:
                    distance = distance_at_hyper
                if speed == 0:
                    return
        """ actual movement """
        self.location = self.location.move(self.waypoints[1].fly_to, distance)
        fuel = self.burn_fuel(speed, num_denials, distance, fuel)
        self.distribute_fuel(fuel, fleet_fuel_max)
    
    """ Spends the fuel and tells the ship to calculate the damage (if there is any) """
    def burn_fuel(self, speed, num_denials, distance, fuel):
        fuel_1_ly = 0
        for ship in self.ships:
            fuel_1_ly += ship.fuel_check(speed, num_denials, distance)
        fuel -= fuel_1_ly
        return fuel
    
    """ Checks if you have the fuel to move at a certain speed with your entire fleet """
    def test_fuel(self, speed, num_denials, distance, fuel):
        fuel_1_ly = 0
        for ship in self.ships:
            fuel_1_ly += ship.fuel_check(speed, num_denials, distance)
        if (fuel - fuel_1_ly) < 0:
            return True
        return False
        
    """ Checks if you can safely move at a certain speed with your entire fleet """
    def test_damage(self, speed, num_denials):
        for ship in self.ships:
            if ship.speed_is_damaging(speed, num_denials) != False:
                return ship.speed_is_damaging(speed, num_denials)
        return False
    
    """ Evenly distributes the fuel between the ships """
    def distribute_fuel(self, fuel, fleet_fuel_max):
        if fleet_fuel_max == 0:
            return
        fuel_left = fuel
        for ship in self.ships:
            ship.fuel = int(fuel * ship.fuel_max / fleet_fuel_max)
            fuel_left -= ship.fuel
        for i in range(int(fuel_left)):
            self.ships[i].fuel += 1
    
    """ Evenly distributes the cargo back to the ships """
    def distribute_cargo(self, cargo, cargo_type, fleet_cargo_max):
        if fleet_cargo_max == 0:
            return
        cargo_left = cargo
        for ship in self.ships:
            ship.cargo[cargo_type] = int(cargo[cargo_type] * ship.cargo.cargo_max / fleet_cargo_max)
            cargo_left[cargo_type] -= ship.cargo[cargo_type]
        for i in range(int(cargo_left[cargo_type])):
            ship = min(self.ships, key=lambda x:x.cargo.percent_full())
            ship.cargo[cargo_type] += 1
    
    """ Gathers all of the cargo from the ships to the fleet """
    def get_cargo(self):
        fleet_cargo_max = 0
        fleet_cargo = Cargo()
        for ship in self.ships:
            fleet_cargo += ship.cargo
            fleet_cargo_max = copy.copy(ship.cargo.cargo_max)
        return fleet_cargo, fleet_cargo_max

    """ Gathers all of the fuel from the ships to the fleet """
    def get_fuel(self):
        fleet_fuel_max = 0
        fleet_fuel = 0
        for ship in self.ships:
            fleet_fuel_max += ship.fuel_max
            fleet_fuel += ship.fuel
        return fleet_fuel, fleet_fuel_max
    
    """ Tells all of its ships to deploy their hyper denial """
    def deploy_hyper_denial(self, player):
        for ship in self.ships:
            ship.deploy_hyper_denial(player)
            
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
