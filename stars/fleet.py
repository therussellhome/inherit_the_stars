import sys
from . import game_engine
from .defaults import Defaults
from .cargo import Cargo
from .player import Player
from .planet import Planet
from .ship import Ship
from .reference import Reference
from .location import Location
from .location import locationReference
from .waypoint import Waypoint


""" Default values (default, min, max)  """
__defaults = {
    'waypoints': [[]],
    'anti_cloak_scanner': [0, 0, sys.maxsize],
    'normal_scanner': [0, 0, sys.maxsize],
    'pennetrating_scaner': [0, 0, sys.maxsize],
    'fuel': [0, 0, sys.maxsize],
    'fuel_max': [0, 0, sys.maxsize],
    'ships': [[]],
    'player': [Reference()],
    'location': [Location()],
    'cargo': [Cargo()]
}


""" Class defining fleets - directly modifiable by the player """
class Fleet(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)
    
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
    
    """  """
    def compile_hyper_denial(self):
        hyper_range = 0
        self.hyper_denial = False
        denial = []
        for ship in self.ships:
            if ship.hyper_denial == True:
                self.hyper_denial = True
                denail.append(ship.hyper_denial_range)
        if self.hyper_denial:
            for i in range(len(denial)):
                if denial[i] >= hyper_range:
                    hyper_range = denial[i]
        self.hyper_denial_range = hyper_range
    
    """ calculates the scaning of the fleet from curent position """
    def calculate_scanning(self):
        self.compile_scanning()
        for ship in game_engine.get('Ship/'):
            if ship.player != self.player:
                ship.mass = ship.hull_masss + (ship.cargo.titanium + ship.cargo.lithium + ship.cargo.silicon + ship.cargo.people)
                ship.aparant_mass = (ship.mass * ship.cloak)
                if ship.player.race.primary_race_trait == "SS":
                    ship.aparant_mass -= ship.kt_modifier
                distance = ((ship.x - self.x)**2 + (ship.y - self.y)**2 + (ship.z - self.z)**2)**(1/2)
                if distance <= self.anti_cloak_scanner:
                    self.player.create_intel_on(ship, ship.mass, True)
                elif distance <= self.pennetrating_scanner and ship.aparant_mass > 0:
                    self.player.create_intel_on(ship, ship.aparant_mass)
                elif distance <= (self.pennetrating_scanner + ((self.normal_scanner - self.pennetrating_scanner) * (ship.aparant_mass / 100))) and ship.aparant_mass > 0:
                    self.player.create_intel_on(ship, ship.aparant_mass)
        for planet in game_engine.get('Planet/'):
            if planet.player != self.player:
                planet.space_station.mass = planet.space_station.design.mass
                planet.space_station.aparant_mass = (planet.space_station.mass * planet.space_station.cloak)
                if planet.player.race.primary_race_trait == "SS":
                    planet.space_station.aparant_mass -= planet.space_station.kt_modifier
                distance = ((planet.x - self.x)**2 + (planet.y - self.y)**2 + (planet.z - self.z)**2)**(1/2)
                if distance <= self.pennetrating_scanner:
                    self.player.create_intel_on(planet, "planet")
                    if distance <= self.anti_cloak_scanner:
                        self.player.create_intel_on(planet.space_station, planet.space_station.mass, True)
                    elif planet.space_station.aparant_mass > 0:
                        self.player.create_intel_on(planet.space_station, planet.space_station.aparant_mass)
    
    """ does all the moving calculations and then moves the ships """
    def move(self, hyper_denials):
        in_hyper_denial = False
        for ship in self.ships:
            self.fuel += ship.fuel
            if 
        for hyper_denial in hyper_denials:
            distance_to_denial = ((hyper_denial.x - self.x)**2 + (hyper_denial.y - self.y)**2 + (hyper_denial.z - self.z)**2)**(1/2)
            if distance_to_denial >= hyper_denial.range:
                in_hyper_denial = True
        speed = waypoints[1].speed
        distance_to_waypoint = ((waypoints[1].fly_to.x - self.x)**2 + (waypoints[1].fly_to.y - self.y)**2 + (waypoints[1].fly_to.z - self.z)**2)**(1/2)
        distance_at_hyper = (speed**2)/100
        if distance_to_waypoint < distance_at_hyper:
            distance = distance_to_waypoint
        else:
            distance = distance_at_hyper
        if distance_to_waypoint == 0:
            #???
        while self.test_move_ly(self.fuel, speed, in_hyper_denial, distance):
            speed -= 1
            distance_at_hyper = (speed**2)/100
            if distance_to_waypoint < distance_at_hyper:
                distance = distance_to_waypoint
            else:
                distance = distance_at_hyper
        self.x, self.y, self.z = self.move_ly(self.fuel, speed, in_hyper_denial, distance)
        self.returnn()
    
    """ calles the move for each of the ships """
    def move_ly(self, fuel, speed, in_hyper_denial=False, dis=1):
        fuel_1_ly = 0
        for ship in self.ships:
            fuel_1_ly += ship.move(speed, in_hyper_denial, dis)
        self.fuel -= fuel_1_ly
        return self.ships[0].x, self.ships[0].y, self.ships[0].z
    
    """ checks if you can move at a certain speed with your entire fleet """
    def test_move_ly(self, fuel, speed, in_hyper_denial=False, dis=1):
        fuel_1_ly = 0
        for ship in self.ships:
            fuel_1_ly += ship.fuel_check(speed, in_hyper_denial, dis)
        if (fuel - fuel_1_ly) >= 0:
            return False
        else:
            return True
        
    """ chooses the ship to return the fuel to """
    def return_cargo(self):
        check = []
        for ship in self.ships:
            ship_percent_cargo = (ship.cargo.titanium + ship.cargo.lithium + ship.cargo.silicon + ship.cargo.people) / ship.cargo.cargo_max
            check.append([ship.persent_cargo, ship])
        least = 1
        lest = 0
        for i in range(len(check)):
            if check[i][0] <= least:
                least = check[i][0]
                lest = i
        return check[lest][1]
    
    """ evenly distributes the fuel between the ships """
    def return_fuel(self):
        check = []
        for ship in self.ships:
            ship_percent_fuel = ship.fuel / ship.max_fuel
            check.append([ship_percent_fuel, ship])
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
        self.cargo.cargo_max = 0
        for ship in self.ships:
            self.cargo.titanium += ship.cargo.titanium
            self.cargo.lithium += ship.cargo.lithium
            self.cargo.silicon += ship.cargo.silicon
            self.cargo.people += ship.cargo.people
            self.cargo.cargo_max += ship.cargo.cargo_max
            ship.cargo.titanium = 0
            ship.cargo.lithium = 0
            ship.cargo.silicon = 0
            ship.cargo.people = 0
            self.fuel_max += ship.fuel_max
            self.fuel += ship.fuel
            ship.fuel = 0
    
    """ executes the unload function """
    def unload(self, recipiant):
        self.compile()
        if recipiant in game_engine.get('Fleet/'):
            recipiant.compile()
        for transfer in self.waypoint.transfers['unload']:
            item = transfer[0]
            amount = transfer[1]
            sum_cargo = (recipiant.cargo.titanium + recipiant.cargo.lithium + recipiant.cargo.silicon + recipiant.cargo.people)
            if item == 'titanium':
                if self.cargo.titanium >= amount and (recipiant.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.titanium -= amount
                    recipiant.cargo.titanium += amount
                elif self.cargo.titanium < amount and (recipiant.cargo.cargo_max - sum_cargo) >= self.cargo.titanium:
                    recipiant.cargo.titanium += self.cargo.titanium
                    self.cargo.titanium = 0
                elif (recipiant.cargo.cargo_max - sum_cargo) < amount and self.cargo.titanium >= (recipiant.cargo.cargo_max - sum_cargo):
                    recipiant.cargo.titanium += (recipiant.cargo.cargo_max - sum_cargo)
                    self.cargo.titanium -= (recipiant.cargo.cargo_max - sum_cargo)
            elif item == 'lithium':
                if self.cargo.lithium >= amount and (recipiant.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.lithium -= amount
                    recipiant.cargo.lithium += amount
                elif self.cargo.lithium < amount and (recipiant.cargo.cargo_max - sum_cargo) >= self.cargo.lithium:
                    recipiant.cargo.lithium += self.cargo.lithium
                    self.cargo.lithium = 0
                elif (recipiant.cargo.cargo_max - sum_cargo) < amount and self.cargo.lithium >= (recipiant.cargo.cargo_max - sum_cargo):
                    recipiant.cargo.lithium += (recipiant.cargo.cargo_max - sum_cargo)
                    self.cargo.lithium -= (recipiant.cargo.cargo_max - sum_cargo)
            elif item == 'silicon':
                if self.cargo.silicon >= amount and (recipiant.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.silicon -= amount
                    recipiant.cargo.silicon += amount
                elif self.cargo.silicon < amount and (recipiant.cargo.cargo_max - sum_cargo) >= self.cargo.silicon:
                    recipiant.cargo.silicon += self.cargo.silicon
                    self.cargo.silicon = 0
                elif (recipiant.cargo.cargo_max - sum_cargo) < amount and self.cargo.silicon >= (recipiant.cargo.cargo_max - sum_cargo):
                    recipiant.cargo.silicon += (recipiant.cargo.cargo_max - sum_cargo)
                    self.cargo.silicon -= (recipiant.cargo.cargo_max - sum_cargo)
            elif item == 'people' and waypoint.description == recipiant:
                if self.cargo.people >= amount and (recipiant.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.people -= amount
                    recipiant.cargo.people += amount
                elif self.cargo.people < amount and (recipiant.cargo.cargo_max - sum_cargo) >= self.cargo.people:
                    recipiant.cargo.people += self.cargo.people
                    self.cargo.people = 0
                elif (recipiant.cargo.cargo_max - sum_cargo) < amount and self.cargo.people >= (recipiant.cargo.cargo_max - sum_cargo):
                    recipiant.cargo.people += (recipiant.cargo.cargo_max - sum_cargo)
                    self.cargo.people -= (recipiant.cargo.cargo_max - sum_cargo)
            elif item == 'fuel':
                if self.fuel >= amount and (recipiant.fuel_max - recipiant.fuel) >= amount:
                    self.fuel -= amount
                    recipiant.fuel += amount
                elif self.fuel < amount and (recipiant.fuel_max - recipiant.fuel) >= self.fuel:
                    recipiant.fuel += self.fuel
                    self.fuel = 0
                elif (recipiant.fuel_max - recipiant.fuel) < amount and self.fuel >= (recipiant.fuel_max - recipiant.fuel):
                    recipiant.fuel += (recipiant.fuel_max - recipiant.fuel)
                    self.fuel -= (recipiant.fuel_max - recipiant.fuel)
        self.returnn()
        if recipiant in game_engine.get('Fleet/'):
            recipiant.returnn()
    
    """ executes the sell function """
    def sell(self, recipiant):
        self.compile()
        for transfer in self.waypoint.transfers['sell']:
            item = transfer[0]
            amount = transfer[1]
            traety = self.player.treaties[recipiant.player.name].sell
            if item == 'titanium' and traety.cost_titanium != None:
                if self.cargo.titanium >= amount:
                    self.cargo.titanium -= amount
                    recipiant.on_surface.titanium += amount
                    self.player.energy += (amount * traety.cost_titanium)
                    recipiant.player.energy -= (amount * traety.cost_titanium)
                else:
                    amount = self.cargo.titanium
                    self.cargo.titanium -= amount
                    recipiant.on_surface.titanium += amount
                    self.player.energy += (amount * traety.cost_titanium)
                    recipiant.player.energy -= (amount * traety.cost_titanium)
            elif item == 'lithium' and traety.cost_lithium != None:
                if self.cargo.lithium >= amount:
                    self.cargo.lithium -= amount
                    recipiant.on_surface.lithium += amount
                    self.player.energy += (amount * traety.cost_lithium)
                    recipiant.player.energy -= (amount * traety.cost_lithium)
                else:
                    amount = self.cargo.lithium
                    self.cargo.lithium -= amount
                    recipiant.on_surface.lithium += amount
                    self.player.energy += (amount * traety.cost_lithium)
                    recipiant.player.energy -= (amount * traety.cost_lithium)
            elif item == 'silicon' and traety.cost_silicon != None:
                if self.cargo.silicon >= amount:
                    self.cargo.silicon -= amount
                    recipiant.on_surface.silicon += amount
                    self.player.energy += (amount * traety.cost_silicon)
                    recipiant.player.energy -= (amount * traety.cost_silicon)
                else:
                    amount = self.cargo.silicon
                    self.cargo.silicon -= amount
                    recipiant.on_surface.silicon += amount
                    self.player.energy += (amount * traety.cost_silicon)
                    recipiant.player.energy -= (amount * traety.cost_silicon)
            elif item == 'fuel' and traety.cost_fuel != None:
                if self.fuel >= amount and (recipiant.space_station.fuel_max - recipiant.space_station.fuel) >= amount:
                    self.fuel -= amount
                    recipiant.space_station.fuel += amount
                    self.player.energy += (amount * traety.cost_fuel)
                    recipiant.player.energy -= (amount * traety.cost_fuel)
                elif self.fuel < amount and (recipiant.space_station.fuel_max - recipiant.space_station.fuel) >= self.fuel:
                    amount = self.fuel
                    self.fuel -= amount
                    recipiant.spase_station.fuel += amount
                    self.player.energy += (amount * traety.cost_fuel)
                    recipiant.player.energy -= (amount * straety.cost_fuel)
                elif (recipiant.spase_station.fuel_max - recipiant.spase_station.fuel) < amount and self.fuel >= (recipiant.spase_station.fuel_max - recipiant.spase_station.fuel):
                    amount = (recipiant.fuel_max - recipiant.fuel)
                    self.fuel -= amount
                    recipiant.spase_station.fuel += amount
                    self.player.energy += (amount * traety.cost_fuel)
                    recipiant.player.energy -= (amount * traety.cost_fuel)
        self.returnn()
    
    """ executes the buy function """
    def buy(self, recipiant):
        self.compile()
        for transfer in self.waypoint.transfers['buy']:
            item = transfer[0]
            amount = transfer[1]
            sum_cargo = (self.cargo.titanium + self.cargo.lithium + self.cargo.silicon + self.cargo.people)
            traety = self.player.treties[recipiant.player.name].buy
            if item == 'titanium' and traety.cost_titanium != None:
                if recipiant.on_surface.titanium >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    recipiant.on_surface.titanium -= amount
                    self.cargo.titinium += amount
                    self.player.energy -= (amount * traety.cost_titanium)
                    recipiant.player.energy += (amount * traety.cost_titanium)
                elif recipiant.on_surface.titanium < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.on_surface.titanium:
                    amount = recipiant.on_surface.titanium
                    recipiant.cargo.titanium -= amount
                    self.cargo.titinium += amount
                    self.player.energy -= (amount * traety.cost_titanium)
                    recipiant.player.energy += (amount * traety.cost_titanium)
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.on_surface.titanium >= (self.cargo.cargo_max - sum_cargo):
                    amount = (self.cargo.cargo_max - sum_cargo)
                    recipiant.on_surface.titanium -= amount
                    self.cargo.titinium += amount
                    self.player.energy -= (amount * traety.cost_titanium)
                    recipiant.player.energy += (amount * traety.cost_titanium)
            elif item == 'lithium' and traety.cost_lithium != None:
                if recipiant.on_surface.lithium >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.lithium += amount
                    recipiant.on_surface.lithium -= amount
                    self.player.energy -= (amount * traety.cost_lithium)
                    recipiant.player.energy += (amount * traety.cost_lithium)
                elif recipiant.on_surface.lithium < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.on_surface.lithium:
                    amount = recipiant.on_surface.lithium
                    self.cargo.lithium += amount
                    recipiant.on_surface.lithium -= amount
                    self.player.energy -= (amount * traety.cost_lithium)
                    recipiant.player.energy += (amount * traety.cost_lithium)
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.on_surface.lithium >= (self.cargo.cargo_max - sum_cargo):
                    amount = (self.cargo.cargo_max - sum_cargo)
                    self.cargo.lithium += amount
                    recipiant.on_surface.lithium -= amount
                    self.player.energy -= (amount * traety.cost_lithium)
                    recipiant.player.energy += (amount * traety.cost_lithium)
            elif item == 'silicon' and traety.cost_silicon != None:
                if recipiant.on_surface.silicon >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.silicon += amount
                    recipiant.on_surface.silicon -= amount
                    self.player.energy -= (amount * traety.cost_silicon)
                    recipiant.player.energy += (amount * traety.cost_silicon)
                elif recipiant.on_surface.silicon < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.on_surface.silicon:
                    amount = recipiant.on_surface.silicon
                    self.cargo.silicon += amount
                    recipiant.on_surface.silicon -= amount
                    self.player.energy -= (amount * traety.cost_silicon)
                    recipiant.player.energy += (amount * traety.cost_silicon)
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.on_surface.silicon >= (self.cargo.cargo_max - sum_cargo):
                    amount = (self.cargo.cargo_max - sum_cargo)
                    self.cargo.silicon += amount
                    recipiant.on_surface.silicon -= amount
                    self.player.energy -= (amount * traety.cost_silicon)
                    recipiant.player.energy += (amount * traety.cost_silicon)
            elif item == 'fuel' and traety.cost_fuel != None:
                if recipiant.space_station.fuel >= amount and (self.fuel_max - self.fuel) >= amount:
                    self.fuel += amount
                    recipiant.space_station.fuel -= amount
                    self.player.energy -= (amount * traety.cost_fuel)
                    recipiant.player.energy += (amount * traety.cost_fuel)
                elif recipiant.space_station.fuel < amount and (self.fuel_max - self.fuel) >= recipiant.space_station.fuel:
                    amount = recipiant.space_station.fuel
                    self.fuel += amount
                    recipiant.space_station.fuel -= amount
                    self.player.energy -= (amount * traety.cost_fuel)
                    recipiant.player.energy += (amount * traety.cost_fuel)
                elif (self.fuel_max - self.fuel) < amount and recipiant.space_station.fuel >= (self.fuel_max - self.fuel):
                    amount = (self.fuel_max - self.fuel)
                    self.fuel += amount
                    recipiant.space_station.fuel -= amount
                    self.player.energy -= (amount * traety.cost_fuel)
                    recipiant.player.energy += (amount * traety.cost_fuel)
        self.returnn()
    
    """ executes the load function """
    def load(self, recipiant):
        self.compile()
        if recipiant in game_engine.get('Fleet/'):
            recipiant.compile()
        for transfer in self.waypoint.transfers['load']:
            item = transfer[0]
            amount = transfer[1]
            sum_cargo = (self.cargo.titanium + self.cargo.lithium + self.cargo.silicon + self.cargo.people)
            if item == 'titanium':
                if recipiant.cargo.titanium >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    recipiant.cargo.titanium -= amount
                    self.cargo.titinium += amount
                elif recipiant.cargo.titanium < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.cargo.titanium:
                    self.cargo.titanium += recipiant.cargo.titanium
                    recipiant.cargo.titanium = 0
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.cargo.titanium >= (self.cargo.cargo_max - sum_cargo):
                    self.cargo.titanium += (self.cargo.cargo_max - sum_cargo)
                    recipiant.cargo.titanium -= (self.cargo.cargo_max - sum_cargo)
            elif item == 'lithium':
                if recipiant.cargo.lithium >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.lithium += amount
                    recipiant.cargo.lithium -= amount
                elif recipiant.cargo.lithium < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.cargo.lithium:
                    self.cargo.lithium += recipiant.cargo.lithium
                    recipiant.cargo.lithium = 0
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.cargo.lithium >= (self.cargo.cargo_max - sum_cargo):
                    self.cargo.lithium += (self.cargo.cargo_max - sum_cargo)
                    recipiant.cargo.lithium -= (self.cargo.cargo_max - sum_cargo)
            elif item == 'silicon':
                if recipiant.cargo.silicon >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.silicon += amount
                    recipiant.cargo.silicon -= amount
                elif recipiant.cargo.silicon < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.cargo.silicon:
                    self.cargo.silicon += recipiant.cargo.silicon
                    recipiant.cargo.silicon = 0
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.cargo.silicon >= (self.cargo.cargo_max - sum_cargo):
                    self.cargo.silicon += (self.cargo.cargo_max - sum_cargo)
                    recipiant.cargo.silicon -= (self.cargo.cargo_max - sum_cargo)
            elif item == 'people':
                if self.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.people += amount
                    recipiant.cargo.people -= amount
                elif recipiant.cargo.people < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.cargo.people:
                    self.cargo.people += recipiant.cargo.people
                    recipiant.cargo.people = 0
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.cargo.people >= (self.cargo.cargo_max - sum_cargo):
                    self.cargo.people += (self.cargo.cargo_max - sum_cargo)
                    recipiant.cargo.people -= (self.cargo.cargo_max - sum_cargo)
            elif item == 'fuel':
                if recipiant.fuel >= amount and (self.fuel_max - self.fuel) >= amount:
                    self.fuel += amount
                    recipiant.fuel -= amount
                elif recipiant.fuel < amount and (self.fuel_max - self.fuel) >= recipiant.fuel:
                    self.fuel += recipiant.fuel
                    recipiant.fuel = 0
                elif (self.fuel_max - self.fuel) < amount and recipiant.fuel >= (self.fuel_max - self.fuel):
                    self.fuel += (self.fuel_max - self.fuel)
                    recipiant.fuel -= (self.fuel_max - self.fuel)
        self.returnn()
        if recipiant in game_engine.get('Fleet/'):
            recipiant.returnn()
    
    """ runs all of the actions """
    def execute(self, action):
        self.waypoint = self.waypoints[0]
        if action in self.waypoint.actions:
            if action == 'unload' or action == 'pre_unload':
                recipiant = self.waypoint.recipiants['unload']
                if recipiant.x == self.x and recipiant.y == self.y and recipiant.z == self.z:
                    if recipiant == "deep_space" or recipiant.name == 'salvage' or recipiant.player == self.player:
                        self.unload(recipiant)
            if action == 'load' or action == 'pre_load':
                recipiant = self.waypoint.recipiants['load']
                if recipiant.x == self.x and recipiant.y == self.y and recipiant.z == self.z:
                    if recipiant.name == 'salvage' or recipiant.player == self.player:
                        self.load(recipiant)
            if action == 'buy' and self.waypoint.recipiants['buy'] in game_engine.get('Planet/') and self.waypoint.recipiants['buy'].space_station.trade:
                recipiant = self.waypoint.recipiants['buy']
                if recipiant.player != self.player:
                    self.buy(recipiant)
            if action == 'sell' and self.waypoint.recipiants['sell'] in game_engine.get('Planet/') and self.waypoint.recipiants['sell'].space_station.trade:
                recipiant = self.waypoint.recipiants['sell']
                if recipiant.player != self.player:
                    self.sell(recipiant)
            
            

""" Ordered list of fleet preactions for use by the Game.generate_turn """
Fleet.preactions = [
    'pre_unload',
    'pre_load',
    'pre_piracy',
]

""" Ordered list of fleet actions for use by the Game.generate_turn """
Fleet.actions = [
    'merge',
    'generate_fuel',
    'self_repair',
    'repair',
    'deploy_hyper_denial',
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
