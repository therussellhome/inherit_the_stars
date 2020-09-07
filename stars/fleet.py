import sys
import copy
from . import stars_math
from . import game_engine
from .cargo import Cargo
from .defaults import Defaults
from .location import Location
from .waypoint import Waypoint
from .location import LocationReference


""" Default values (default, min, max)  """
__defaults = {
    'waypoints': [[]],
    'anti_cloak_scanner': [0, 0, sys.maxsize],
    'normal_scanner': [0, 0, sys.maxsize],
    'pennetrating_scaner': [0, 0, sys.maxsize],
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
                if (self.location - ship.location) <= (stars_math.TERAMETER_2_LIGHTYEAR * 2):
                    self.ships.append(ship)
    
    """ gives the fleet the highest scaner of each type from it's ships """
    def compile_scanning(self):
        max_anti_cloak = 0
        max_normal = 0
        max_penetrating = 0
        scanner = []
        for ship in self.ships:
            scanner.append([ship.anti_cloak_scanner, ship.normal_scanner, self.pennetrating_scanner])
        for i in range(len(scanner)):
            if scanner[i][0] >= max_anti_cloak:
                max_anti_cloak = scanner[i][0]
            if scanner[i][1] >= max_normal:
                max_normal = scanner[i][1]
            if scanner[i][2] >= max_penetrating:
                max_penetrating = scanner[i][2]
        self.anti_cloak_scanner = max_anti_cloak
        self.normal_scanner = max_normal
        self.pennetrating_scanner = max_penetrating
        
    """ checks if can upgrade and then stops moving if comanded to """
    def check_upgrade(self):
        if self.waypoints[1].upgrade_if_commanded == True and self.waypoints[1].location in game_engine.get('Planets/') and self.waypoints[1].location.space_station:
            for ship in self.ships:
                if ship.new_design and ship.new_design.mass <= self.waypoints[1].location.space_station.max_build_mass:
                    self.waypoints[1].location.upgrade(ship)
    
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
        while self.test_fuel(speed, num_denials, distance) and self.test_damage(speed, num_denials):
            speed -= 1
            distance_at_hyper = (speed**2)/100
            if distance_to_waypoint < distance_at_hyper:
                distance = distance_to_waypoint
            else:
                distance = distance_at_hyper
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
        
    """ chooses the ship to return the fuel to """
    def return_cargo(self):
        check = [[(ship.cargo.titanium + ship.cargo.lithium + ship.cargo.silicon + ship.cargo.people) / ship.cargo.cargo_max, ship] for ship in self.ships]
        least = 1
        lest = 0
        for i in range(len(check)):
            if check[i][0] <= least:
                least = check[i][0]
                lest = i
        return check[lest][1]
    
    """ evenly distributes the fuel between the ships """
    def return_fuel(self):
        check = [[ship.fuel / ship.fuel_max, ship] for ship in self.ships]
        least = 1
        lest = 0
        for i in range(len(check)):
            if check[i][0] <= least:
                least = check[i][0]
                lest = i
        return check[lest][1]
    
    """ evenly distributes the cargo back to the ships """
    def returnn(self):
        while self.fuel > 0:
            ship = self.return_fuel()
            ship.fuel += 1
            self.fuel -= 1
        while (self.cargo.titanium + self.cargo.lithium + self.cargo.silicon + self.cargo.people) > 0:
            ship = self.return_cargo()
            if self.cargo.titanium > 0:
                ship.cargo.titanium += 1
                self.cargo.titanium -= 1
            elif self.cargo.lithium > 0:
                ship.cargo.lithium += 1
                self.cargo.lithium -= 1
            elif self.cargo.silicon > 0:
                ship.cargo.silicon += 1
                self.cargo.silicon -= 1
            elif self.cargo.people > 0:
                ship.cargo.people += 1
                self.cargo.people -= 1
    
    """ gathers all of the minerals and fuel from the ships to the fleet """
    def compile(self):
        self.fuel_max = 0
        for ship in self.ships:
            self.cargo += ship.cargo
            cargo_max = copy.copy(ship.cargo.cargo_max)
            ship.cargo = Cargo(cargo_max=cargo_max)
            self.fuel_max += ship.fuel_max
            self.fuel += ship.fuel
            ship.fuel = 0
    
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
        if not self.check_self(recipiant, player):
            return
        self.compile()
        if recipiant in player.fleets:
            recipiant.compile()
            load_fuel_to = recipiant
            load_cargo_to = recipiant.cargo
        else:
            load_fuel_to = recipiant.space_station
            load_cargo_to = recipiant.on_surface
        for transfer in self.waypoints[0].transfers['unload']:
            item = transfer[0]
            amount = transfer[1]
            amount = self.handle_cargo(self, load_fuel_to, item, amount, load_cargo_to, self.cargo)
            if item == 'fuel':
                setattr(load_fuel_to, item, getattr(load_fuel_to, item) + amount)
                setattr(self, item, getattr(self, item) - amount)
            else:
                setattr(load_cargo_to, item, getattr(load_cargo_to, item) + amount)
                setattr(self.cargo, item, getattr(self.cargo, item) - amount)    
        self.returnn()
        if recipiant in player.fleets:
            recipiant.returnn()
    
    """ executes the sell function """
    def sell(self, recipiant, player):
        if not self.check_team(recipiant, player):
            return
        self.compile()
        if recipiant in player.fleets:
            recipiant.compile()
            load_fuel_to = recipiant
            load_cargo_to = recipiant.cargo
        else:
            load_fuel_to = recipiant.space_station
            load_cargo__to = recipiant.on_surface
        for transfer in self.waypoints[0].transfers['sell']:
            item = transfer[0]
            amount = transfer[1]
            traety = player.treaties[recipiant.player.name].sell
            if getattr(traety, "cost_"+item) != None:
                amount = self.handle_cargo(self, load_fuel_to, item, amount, load_cargo_to, self.cargo)
                for i in amount:
                    if recipiant.player.energy_minister.check_budget("trade", getattr(traety, "cost_"+item)) > getattr(traety, "cost_"+item):
                        if item == 'fuel':
                            setattr(load_fuel_to, item, getattr(load_fuel_to, item) - 1)
                            setattr(self, item, getattr(self, item) + 1)
                        else:
                            setattr(load_cargo_to, item, getattr(load_cargo_to, item) - 1)
                            setattr(self.cargo, item, getattr(self.cargo, item) + 1)
                        player.energy_minister.spend_budget("trade", -getattr(traety, "cost_"+item))
                        recipiant.player.energy_minister.spend_budget("trade", getattr(traety, "cost_"+item))
        self.returnn()
    
    def handle_cargo(self, unload_fuel_from, load_fuel_to, item, amount, load_cargo_to, unload_cargo_from):
        print(amount, item, 'with problem', end=' ')
        sum_cargo = (load_cargo_to.titanium + load_cargo_to.silicon + load_cargo_to.lithium + load_cargo_to.people)
        if item in ["fuel", "titanium", "silicon", "lithium", "people"]:
            if item == 'fuel':
                if unload_fuel_from.fuel < amount and (load_fuel_to.fuel_max - load_fuel_to.fuel) >= unload_fuel_from.fuel:
                    print("'not enough "+item+"'", "{'fuel': "+str(unload_fuel_from.fuel)+", 'fuel_max': "+str(unload_fuel_from.fuel_max)+"}", end=' ')
                    amount = unload_fuel_from.fuel
                elif (load_fuel_to.fuel_max - load_fuel_to.fuel) < amount and unload_fuel_from.fuel >= (load_fuel_to.fuel_max - load_fuel_to.fuel):
                    print("'not enough capacity'", "{'fuel': "+str(unload_fuel_from.fuel)+", 'fuel_max': "+str(unload_fuel_from.fuel_max)+"}", end=' ')
                    amount = (load_fuel_to.fuel_max - load_fuel_no.fuel)
                else:
                    print('none', end=' ')
            else:
                if getattr(unload_cargo_from, item) < amount and (load_cargo_to.cargo_max - sum_cargo) >= getattr(unload_cargo_from, item):
                    print("'not enough "+item+"'", unload_cargo_from.__dict__, end=' ')
                    amount = getattr(unload_cargo_from, item)
                elif (load_cargo_to.cargo_max - sum_cargo) < amount and getattr(unload_cargo_from, item) >= (load_cargo_to.cargo_max - sum_cargo):
                    print("'not enough capacity'", unload_cargo_from.__dict__, end=' ')
                    amount = (load_cargo_to.cargo_max - sum_cargo)
                else:
                    print('none', end=' ')
        
        print('becomes', amount)
        return amount
    
    """ executes the buy function """
    def buy(self, recipiant, player):
        if not self.check_team(recipiant, player):
            return
        self.compile()
        if recipiant in player.fleets:
            recipiant.compile()
            unload_fuel_from = recipiant
            unload_cargo_from = recipiant.cargo
        else:
            unload_fuel_from = recipiant.space_station
            unload_cargo_from = recipiant.on_surface
        for transfer in self.waypoints[0].transfers['buy']:
            item = transfer[0]
            amount = transfer[1]
            traety = player.treaties[recipiant.player.name].sell
            if getattr(traety, "cost_"+item) != None:
                amount = self.handle_cargo(unload_fuel_from, self, item, amount, self.cargo, unload_cargo_from)
                for i in amount:
                    if recipiant.player.energy_minister.check_budget("trade", getattr(traety, "cost_"+item)) > getattr(traety, "cost_"+item):
                        if item == 'fuel':
                            setattr(unload_fuel_from, item, getattr(unload_fuel_from, item) + 1)
                            setattr(self, item, getattr(self, item) - 1)
                        else:
                            setattr(unload_cargo_from, item, getattr(unload_cargo_from, item) + 1)
                            setattr(self.cargo, item, getattr(self.cargo, item) - 1)
                        player.energy_minister.check_budget("trade", getattr(traety, "cost_"+item))
                        recipiant.player.energy_minister.check_budget("trade", -getattr(traety, "cost_"+item))
        self.returnn()
        
    """ telles the ships in the fleet that can colonize to colonize the planet """
    def colonize(self, player):
        planet = self.waypoints[0].location
        if planet.player.is_valid:
            return
        for ship in self.ships:
            ship.colonize(player, planet)
    
    """ scraps the fleet """
    def scrap(self):
        for ship in ships:
            ship.scrap(fleet.location)
    
    def check_self(self, recipiant, player):
        if recipiant in player.fleets:
            print('Fleet-Yours')
            return True
        if recipiant in game_engine.get('Planet/'):
            print('\nPlanet-', end='')
            if recipiant.player == player:
                print('Yours')
                return True
            print('Nither')
            print(recipiant.player.name)
            print(player.name)
        return False
    
    def check_team(self, recipiant, player):
        if recipiant in game_engine.get('Planet/'):
            if recipiant.player.treaties[player.name].relation == "team":
                if player.treaties[recipiant.player.name].relation == "team":
                    return True
        return False
    
    """ executes the load function """
    def load(self, recipiant, player):
        if not self.check_self(recipiant, player):
            return
        self.compile()
        if recipiant in player.fleets:
            recipiant.compile()
            unload_fuel_from = recipiant
            unload_cargo_from = recipiant.cargo
        else:
            unload_fuel_from = recipiant.space_station
            unload_cargo_from = recipiant.on_surface
        for transfer in self.waypoints[0].transfers['load']:
            item = transfer[0]
            amount = transfer[1]
            amount = self.handle_cargo(unload_fuel_from, self, item, amount, self.cargo, unload_cargo_from)
            if item == 'fuel':
                setattr(unload_fuel_from, item, getattr(unload_fuel_from, item) - amount)
                setattr(self, item, getattr(self, item) + amount)
            else:
                setattr(unload_cargo_from, item, getattr(unload_cargo_from, item) - amount)
                setattr(self.cargo, item, getattr(self.cargo, item) + amount)    
        self.returnn()
        if recipiant in player.fleets:
            recipiant.returnn()
    
    def repair(self, player):
        repair_points = 0
        for ship in self.ships:
            repair_points += ship.open_repair_bays()
        for fleet in player.fleets:
            if (self.location - fleet.location) <= (2 * stars_math.TERAMETER_2_LIGHTYEAR):
                for ship in fleet:
                    ships_here.append(ship)
        self.distribute_repair(ships_here, repair_points)
    
    def distribute_repair(self, ships_here, repair_points):
        while repair_points > 0 and self.find_repair(ships_here) != False:
            ship = self.find_repair(ships_here)
            ship.repair(1)
            repair_points -= 1
    
    def find_repair(self, ships_here):
        damage_ratio = []
        for ship in ships_here:
            damage_ratio.append([100 * (ship.armor / ship.max_armor), ship])
        damage = 100
        worst = 0
        for i in range(len(damage_ratio)):
            if damage_ratio[i][0] <= damage:
                damage = damage_ratio[i][0]
                worst = i
        if damage_ratio[worst][0] == 100:
            return False
        return dmage_ratio[worst][1]
    
    def lay_mines(self, player):
        system = self.waypoints[0].recipiants['lay_mines']
        for ship in self.ships:
            ship.lay_mines(player, system)
    
    def self_repair(self):
        for ship in self.ships:
            ship.self_repair()
    
    def orbital_mining(self):
        planet = self.waypoints[0].recipiants['orbital_mining']
        if planet not in game_engine.get('Planet/') or planet.on_surface.people != 0:
            return
        for ship in self.ships:
            ship.orbital_mining(planet)
    
    def scan(self, player):
        for ship in self.ships:
            ship.scan(player)
    
    def bomb(self, player):
        planet = self.waypoints[0].recipiants['bomb']
        if planet in game_engine.get('Planet/') and planet.player != player and planet.player.is_valid and player.treaties[planet.player.name].relation == 'enemy':
            for ship in self.ships:
                ship.bomb(planet)
    
    """ runs all of the actions """
    def execute(self, action, player):
        if action == 'scan':
            self.scan(player)
        elif action == 'move':
            self.move(player)
        elif action in self.waypoints[0].actions and (self.waypoints[0].location - self.location) <= (2 * stars_math.TERAMETER_2_LIGHTYEAR):
            if action == 'unload' or action == 'pre_unload':
                self.unload(self.waypoints[0].recipiants['unload'], player)
            elif action == 'load' or action == 'pre_load':
                self.load(self.waypoints[0].recipiants['load'], player)
            elif action == 'buy':
                recipiant = self.waypoints[0].recipiants['buy']
                if recipiant in game_engine.get('Planet/') and recipiant.space_station.trade:
                    self.buy(recipiant, player)
            elif action == 'sell':
                recipiant = self.waypoints[0].recipiants['sell']
                if recipiant in game_engine.get('Planet/') and recipiant.space_station.trade:
                    self.sell(recipiant, player)
            elif action == 'deploy_hyper_denial' and self.waypoints[1].deploy_hyper_denial_time > 0:
                self.waypoints[1].deploy_hyper_denial_time -= 1
                self.deploy_hyper_denial(player)
            elif action == 'merge':
                self.merge(player)
            elif action == 'split':
                self.split(player)
            elif action == 'transfer':
                self.transfer(player)
            elif action == 'colonize':
                self.colonize(player)
            elif action == 'lay_mines':
                self.lay_mines(player)
            elif action == 'scrap':
                self.scrap()
            elif action == 'repair':
                self.repair(player)
            elif action == 'orbital_mining':
                self.orbital_mining()
            elif action == 'self_repair':
                self.self_repair()
            elif action == 'bomb':
                self.bomb(player)
            
Fleet.set_defaults(Fleet, __defaults)

""" Ordered list of fleet preactions for use by the Game.generate_turn """
Fleet.preactions = [
    'pre_unload',
    'pre_load',
    'pre_piracy',
    'deploy_hyper_denial',
]

""" Ordered list of fleet actions for use by the Game.generate_turn """
Fleet.actions = [
    'merge',
    'generate_fuel',#move to starbase
    'self_repair',
    'repair',
    'orbital_mining',
    'lay_mines',
    'bomb',
    'colonize',
    'piracy',
    'sell',
    'unload',
    'scrap',
    'buy',
    'load',
    'transfer',
    'patrol',
    'route',
]
