import sys
import copy
from . import stars_math
from . import game_engine
from .cargo import Cargo
from .defaults import Defaults
from .location import Location
from .waypoint import Waypoint
from .location import LocationReference
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'waypoints': [[]],
    'fuel': [0, 0, sys.maxsize],
    'fuel_max': [0, 0, sys.maxsize],
    'ships': [[]],
    'cargo': [Cargo()],
    'location':[Location()]
}


""" Class defining fleets - directly modifiable by the player """
class Fleet(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'Fleet #'+str(hex(id(self)))[-7:-1]
    
    """ adds the ships to self.ships """
    def add_ships(self, ships):
        for ship in ships:
            if len(self.ships) == 0:
                self.location = copy.copy(ship.location)
                self.ships.append(ship)
            else:
                if (self.location - ship.location) <= (stars_math.TERAMETER_2_LIGHTYEAR * 2) and ship not in self.ships:
                    self.ships.append(ship)
    
    #""" checks if can upgrade and then stops moving if comanded to """
    #def check_upgrade(self, player):
    #    if self.waypoints[1].upgrade_if_commanded == True and self.waypoints[1].location in game_engine.get('Planets/') and self.waypoints[1].location.space_station:
    #        for ship in self.ships:
    #            if ship.new_design and ship.new_design.mass <= self.waypoints[1].location.space_station.max_build_mass:
    #                self.waypoints[1].location.upgrade(ship)
    
    """ does all the moving calculations and then moves the ships """
    def move(self, player):
        self.waypoints[1].move_to(self)
        num_denials = 0
        for ship in self.ships:
            self.fuel += ship.fuel
        #for hyper_denial in game_engine.hyper_denials:
        #    distance_to_denial = self.location - hyper_denial.location
        #    if distance_to_denial >= hyper_denial.range and hyper_denial.player.treaties[player.name].relation == 'enemy':
        #        num_denials += 1
        speed = self.waypoints[1].speed
        distance_to_waypoint = self.location - self.waypoints[1].fly_to
        distance_at_hyper = (speed**2)/100
        if distance_to_waypoint < distance_at_hyper:
            distance = distance_to_waypoint
        else:
            distance = distance_at_hyper
        if distance_to_waypoint == 0:
            if self.waypoints[2] and self.waypoints[2].location - self.location != 0:
                self.waypoints.pop(0)
                self.move(player)
            else:
                return
        while self.test_fuel(speed, num_denials, distance) or self.test_damage(speed, num_denials):
            speed -= 1
            distance_at_hyper = (speed**2)/100
            if distance_to_waypoint < distance_at_hyper:
                distance = distance_to_waypoint
            else:
                distance = distance_at_hyper
            if speed == 0:
                return
        self.location = self.location.move(self.waypoints[1].fly_to, distance)
        self.burn_fuel(speed, num_denials, self.waypoints[1].fly_to, distance)
        self.returnn()
    
    """ calles the move for each of the ships """
    def burn_fuel(self, speed, num_denials, fly_to, distance):
        fuel_1_ly = 0
        for ship in self.ships:
            fuel_1_ly += ship.move(speed, num_denials, fly_to, distance)
        self.fuel -= fuel_1_ly
    
    """ checks if you can move at a certain speed with your entire fleet """
    def test_fuel(self, speed, num_denials, dis):
        fuel_1_ly = 0
        for ship in self.ships:
            fuel_1_ly += ship.fuel_check(speed, num_denials, dis)
        if (self.fuel - fuel_1_ly) >= 0:
            return False
        else:
            return True
        
    """ checks if you can move at a certain speed with your entire fleet """
    def test_damage(self, speed, num_denials):
        for ship in self.ships:
            if not ship.speed_is_damaging(speed, num_denials):
                return False
        return True
    
    """ evenly distributes the fuel between the ships """
    def distribute_fuel(self, fuel, fleet_fuel_max):
        if fleet_fuel_max == 0:
            return
        fuel_left = fuel
        for ship in self.ships:
            ship.fuel = int(fuel * ship.fuel_max / fleet_fuel_max)
            fuel_left -= ship.fuel
        for i in range(fuel_left):
            self.ships[i].fuel += 1
    
    """ evenly distributes the cargo back to the ships """
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
    
    """ gathers all of the cargo from the ships to the fleet """
    def get_cargo(self):
        fleet_cargo_max = 0
        fleet_cargo = Cargo()
        for ship in self.ships:
            fleet_cargo += ship.cargo
            fleet_cargo_max = copy.copy(ship.cargo.cargo_max)
        return fleet_cargo, fleet_cargo_max

    """ gathers all of the fuel from the ships to the fleet """
    def get_fuel(self):
        fleet_fuel_max = 0
        fleet_fuel = 0
        for ship in self.ships:
            fleet_fuel_max += ship.fuel_max
            fleet_fuel += ship.fuel
        return fleet_fuel, fleet_fuel_max
    
    """ makes a hyper_denial """
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
    
    """ splits the fleet """
    def split(self, player):
        for split in self.waypoints[0].splits:
            player.create_fleet(ships = split, waypoints = copy.copy(self.waypoints))
            for ship in split:
                self.ships.remove(ship)
        if len(self.ships) == 0:
            player.remove_fleet(self)
    
    """ transfers the fleet """
    def transfer(self, player):
        player_2 = self.waypoints[0].recipiants['transfer']
        self.waypoints = []
        player_2.add_fleet(self)
        if self in player_2.fleets:
            player.remove_fleet(self)
    
    """ executes the unload function """
    def unload(self, recipiant, player):
        if not self.check_self(recipiant, player) and not recipiant.is_colonized():
            return
        self_cargo, self_cargo_max = self.get_cargo()
        self_fuel, self_fuel_max = self.get_fuel()
        if recipiant in player.fleets:
            load_cargo, load_cargo_max = recipiant.get_cargo()
            load_fuel, load_fuel_max = recipiant.get_fuel()
        else:
            load_fuel = recipiant.space_station.fuel
            load_fuel_max = recipiant.space_station.fuel_max
            load_cargo = recipiant.on_surface
            load_cargo_max = recipiant.on_surface.cargo_max
        for transfer in self.waypoints[0].transfers['unload']:
            item = transfer[0]
            amount = transfer[1]
            amount = self.handle_cargo(self_fuel, load_fuel, load_fuel_max, item, amount, load_cargo, load_cargo_max, self_cargo)
            if item == 'fuel':
                load_fuel += amount
                self_fuel -= amount
            else:
                load_cargo[item] += amount
                self_cargo[item] -= amount
        for item in ["titanium", "silicon", "lithium", "people"]:
            self.distribute_cargo(self_cargo, item, self_cargo_max)
        self.distribute_fuel(self_fuel, self_fuel_max)
        print('loaded sucsesfully?')
        if recipiant in player.fleets:
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.distribute_cargo(load_cargo, item, load_cargo_max)
            recipiant.distribute_fuel(load_fuel, load_fuel_max)
        else:
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.on_surface[item] = load_cargo[item]
            recipiant.space_station.fuel = load_fuel
    
    """ executes the sell function """
    def sell(self, recipiant, player):
        if not self.check_team(recipiant, player):
            return
        self_cargo, self_cargo_max = self.get_cargo()
        self_fuel, self_fuel_max = self.get_fuel()
        if recipiant.__class__.__name__ == 'fleet':
            load_cargo, load_cargo_max = recipiant.get_cargo()
            load_fuel, load_fuel_max = recipiant.get_fuel()
        else:
            load_fuel = recipiant.space_station.fuel
            load_fuel_max = recipiant.space_station.fuel_max
            load_cargo = recipiant.on_surface
            load_cargo_max = recipiant.on_surface.cargo_max
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
                if item == 'fuel':
                    load_fuel += true_amount
                    self_fuel -= true_amount
                else:
                    load_cargo[item] += true_amount
                    self_cargo[item] -= true_amount
                player.energy += recipiant.player.spend('trade', traety['sell_' + abreve] * true_amount)
        for item in ["titanium", "silicon", "lithium", "people"]:
            self.distribute_cargo(self_cargo, item, self_cargo_max)
        self.distribute_fuel(self_fuel, self_fuel_max)
        if recipiant.__class__.__name__ == 'fleet':
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.distribute_cargo(load_cargo, item, load_cargo_max)
            recipiant.distribute_fuel(load_fuel, load_fuel_max)
        else:
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.on_surface[item] = load_cargo[item]
            recipiant.space_station.fuel = load_fuel
    
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
    
    """ executes the buy function """
    def buy(self, recipiant, player):
        if not self.check_team(recipiant, player):
            return
        self_cargo, self_cargo_max = self.get_cargo()
        self_fuel, self_fuel_max = self.get_fuel()
        if recipiant.__class__.__name__ == 'fleet':
            unload_cargo, unload_cargo_max = recipiant.get_cargo()
            unload_fuel, unload_fuel_max = recipiant.get_fuel()
        else:
            unload_fuel = recipiant.space_station.fuel
            unload_cargo = recipiant.on_surface
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
                if item == 'fuel':
                    unload_fuel -= true_amount
                    self_fuel += true_amount
                else:
                    unload_cargo[item] -= true_amount
                    self_cargo[item] += true_amount
                recipiant.player.energy += player.spend('trade', traety['buy_' + abreve] * true_amount)
        for item in ["titanium", "silicon", "lithium", "people"]:
            self.distribute_cargo(self_cargo, item, self_cargo_max)
        self.distribute_fuel(self_fuel, self_fuel_max)
        if recipiant.__class__.__name__ == 'fleet':
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.distribute_cargo(unload_cargo, item, unload_cargo_max)
            recipiant.distribute_fuel(unload_fuel, unload_fuel_max)
        else:
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.on_surface[item] = unload_cargo[item]
            recipiant.space_station.fuel = unload_fuel
        
    """ telles the ships in the fleet that can colonize to colonize the planet """
    def colonize(self, player):
        planet = self.waypoints[0].recipiants['colonize']
        if planet.player.is_valid:
            return
        for ship in self.ships:
            if ship.colonizer and ship.cargo.people > 0:
                ship.colonize(Reference(player), planet)
                ship.scrap(planet, self.location)
                self.ships.remove(ship)
                break
    
    """ scraps the fleet """
    def scrap(self):
        try:
            planet = self.waypoints[0].recipiants['scrap']
            for ship in self.ships:
                ship.scrap(planet, self.location)
        except:
            planet = self.location
            for ship in self.ships:
                ship.scrap(planet, self.location)
    
    def check_self(self, recipiant, player):
        if recipiant in player.fleets:
            print('Fleet-Yours')
            return True
        if recipiant in game_engine.get('Planet'):
            print('Planet-', end='')
            if recipiant.player.name == player.name:
                print('Yours')
                return True
            print('Other')
            print(recipiant.player.name)
            print(player.name)
        return False
    
    def check_team(self, recipiant, player):
        if recipiant in game_engine.get('Planet'):
            if player.get_treaty(recipiant.player).relation == 'team' and player.get_treaty(recipiant.player).status == 'active':
                return True
        return False
    
    """ executes the load function """
    def load(self, recipiant, player):
        if not self.check_self(recipiant, player):
            return
        self_cargo, self_cargo_max = self.get_cargo()
        self_fuel, self_fuel_max = self.get_fuel()
        if recipiant in player.fleets:
            unload_cargo, unload_cargo_max = recipiant.get_cargo()
            unload_fuel, unload_fuel_max = recipiant.get_fuel()
        else:
            unload_fuel = recipiant.space_station.fuel
            unload_cargo = recipiant.on_surface
        for transfer in self.waypoints[0].transfers['load']:
            item = transfer[0]
            amount = transfer[1]
            amount = self.handle_cargo(unload_fuel, self_fuel, self_fuel_max, item, amount, self_cargo, self_cargo_max, unload_cargo)
            if item == 'fuel':
                unload_fuel -= amount
                self_fuel +=  amount
            else:
                unload_cargo[item] -= amount
                self_cargo[item] += amount
        for item in ["titanium", "silicon", "lithium", "people"]:
            self.distribute_cargo(self_cargo, item, self_cargo_max)
        self.distribute_fuel(self_fuel, self_fuel_max)
        print('unloaded sucsesfully?')
        if recipiant in player.fleets:
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.distribute_cargo(unload_cargo, item, unload_cargo_max)
            recipiant.distribute_fuel(unload_fuel, unload_fuel_max)
        else:
            for item in ["titanium", "silicon", "lithium", "people"]:
                recipiant.on_surface[item] = unload_cargo[item]
            recipiant.space_station.fuel = unload_fuel
    
    def repair(self, player):
        repair_points = 0
        ships_here = []
        for ship in self.ships:
            repair_points += ship.open_repair_bays()
        for fleet in player.fleets:
            if (self.location - fleet.location) == 0:
                for ship in fleet.ships:
                    ships_here.append(ship)
        self.distribute_repair(ships_here, repair_points)
    
    def distribute_repair(self, ships_here, repair_points):
        while repair_points > 0 and self.find_repair(ships_here) != False:
            self.find_repair(ships_here).repair_self(1)
            repair_points -= 1
    
    def find_repair(self, ships_here):
        repair_me = ships_here[0]
        damage = 0
        for ship in ships_here:
            if damage < ship.damage_armor / ship.armor:
                repair_me = ship
        return repair_me
    
    def lay_mines(self, player):
        system = self.waypoints[0].recipiants['lay_mines']
        for ship in self.ships:
            ship.lay_mines(player, system)
    
    def self_repair(self):
        repair_points = 0
        for ship in self.ships:
            repair_points += ship.damage_control()
        self.distribute_repair(self.ships, repair_points)
    
    def orbital_mining(self):
        planet = self.waypoints[0].recipiants['orbital_mining']
        if planet not in game_engine.get('Planet'):
            return
        for ship in self.ships:
            ship.orbital_mining(planet)
    
    def patrol(self, player):
        pass #TODO
    
    def piracy(self, player):
        pass #TODO
    
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
            print(planet.on_surface.people)

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
