import sys
from . import game_engine
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'waypoints': [[]],
}


""" Class defining fleets - directly modifiable by the player """
class Fleet(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)
    
    def move(self):
        top_speed = waypoints[1].speed
        move = True
        has_moved = False
        time = 0
        for ship in self.ships:
            self.fuel += ship.fuel
        while move:
            speed = top_speed
            while self.test_move_1_ly(self.fuel, speed):
                self.test_move_1_ly(self.fuel, speed)
                speed -= 1
                time += 1/(speed**2)
                if time >= 1:
                    move = False
            if not move:
                break
            self.move_1_ly(self.fuel, speed)
    
    def move_1_ly(self, fuel, speed):
        fuel_1_ly = 0
        for ship in self.ships:
            fuel_1_ly += ship.move_1_ly(speed)
        self.fuel -= fuel_1_ly
    
    def test_move_1_ly(self, fuel, speed):
        fuel_1_ly = 0
        for ship in self.ships:
            fuel_1_ly += ship.test_move_1_ly(speed)
        if (fuel - fuel_1_ly) >= 0:
            return False
        else:
            return True
        
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
    
    def return_fuel(self):
        check = []
        for ship in self.ships:
            ship_percent_fuel = ship.fuel / ship.max_fuel
            check.append([ship.percent_fuel, ship])
        least = 1
        lest = 0
        for i in range(len(check)):
            if check[i][0] <= least:
                least = check[i][0]
                lest = i
        return check[lest][1]
    
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
    
    def compile(self):
        for ship in self.ships:
            self.cargo.titanium += ship.cargo.titanium
            self.cargo.lithium += ship.cargo.lithium
            self.cargo.silicon += ship.cargo.silicon
            self.cargo.people += ship.cargo.people
            ship.cargo.titanium = 0
            ship.cargo.lithium = 0
            ship.cargo.silicon = 0
            ship.cargo.people = 0
            self.fuel += ship.fuel
            ship.fuel = 0
    
    def unload(self):
        self.compile()
        for transfer in self.waypoint.unload.transfers:
            item = transfer[0]
            amount = transfer[1]
            recipiant = self.waypoint.unload.recipiant
            sum_cargo = (recipiant.cargo.titanium + recipiant.cargo.lithium + recipiant.cargo.silicon + recipiant.cargo.people)
            if item == "titanium":
                if self.cargo.titanium >= amount and (recipiant.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.titanium -= amount
                    recipiant.cargo.titinium += amount
                elif self.cargo.titanium < amount and (recipiant.cargo.cargo_max - sum_cargo) >= self.cargo.titanium:
                    recipiant.cargo.titanium += self.cargo.titanium
                    self.cargo.titanium = 0
                elif (recipiant.cargo.cargo_max - sum_cargo) < amount and self.cargo.titanium >= (recipiant.cargo.cargo_max - sum_cargo):
                    recipiant.cargo.titanium += (recipiant.cargo.cargo_max - sum_cargo)
                    self.cargo.titanium -= (recipiant.cargo.cargo_max - sum_cargo)
            elif item == "lithium":
                if self.cargo.lithium >= amount and (recipiant.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.lithium -= amount
                    recipiant.cargo.lithium += amount
                elif self.cargo.lithium < amount and (recipiant.cargo.cargo_max - sum_cargo) >= self.cargo.lithium:
                    recipiant.cargo.lithium += self.cargo.lithium
                    self.cargo.lithium = 0
                elif (recipiant.cargo.cargo_max - sum_cargo) < amount and self.cargo.lithium >= (recipiant.cargo.cargo_max - sum_cargo):
                    recipiant.cargo.lithium += (recipiant.cargo.cargo_max - sum_cargo)
                    self.cargo.lithium -= (recipiant.cargo.cargo_max - sum_cargo)
            elif item == "silicon":
                if self.cargo.silicon >= amount and (recipiant.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.silicon -= amount
                    recipiant.cargo.silicon += amount
                elif self.cargo.silicon < amount and (recipiant.cargo.cargo_max - sum_cargo) >= self.cargo.silicon:
                    recipiant.cargo.silicon += self.cargo.silicon
                    self.cargo.silicon = 0
                elif (recipiant.cargo.cargo_max - sum_cargo) < amount and self.cargo.silicon >= (recipiant.cargo.cargo_max - sum_cargo):
                    recipiant.cargo.silicon += (recipiant.cargo.cargo_max - sum_cargo)
                    self.cargo.silicon -= (recipiant.cargo.cargo_max - sum_cargo)
            elif item == "people":
                if self.cargo.people >= amount and (recipiant.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.people -= amount
                    recipiant.cargo.people += amount
                elif self.cargo.people < amount and (recipiant.cargo.cargo_max - sum_cargo) >= self.cargo.people:
                    recipiant.cargo.people += self.cargo.people
                    self.cargo.people = 0
                elif (recipiant.cargo.cargo_max - sum_cargo) < amount and self.cargo.people >= (recipiant.cargo.cargo_max - sum_cargo):
                    recipiant.cargo.people += (recipiant.cargo.cargo_max - sum_cargo)
                    self.cargo.people -= (recipiant.cargo.cargo_max - sum_cargo)
            elif item == "fuel":
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
    
    def load(self):
        self.compile()
        for transfer in self.waypoint.load.transfers:
            item = transfer[0]
            amount = transfer[1]
            recipiant = self.waypoint.load.recipiant
            sum_cargo = (self.cargo.titanium + self.cargo.lithium + self.cargo.silicon + self.cargo.people)
            if item == "titanium":
                if recipiant.cargo.titanium >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    recipiant.cargo.titanium -= amount
                    self.cargo.titinium += amount
                elif recipiant.cargo.titanium < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.cargo.titanium:
                    self.cargo.titanium += recipiant.cargo.titanium
                    recipiant.cargo.titanium = 0
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.cargo.titanium >= (self.cargo.cargo_max - sum_cargo):
                    self.cargo.titanium += (self.cargo.cargo_max - sum_cargo)
                    recipiant.cargo.titanium -= (self.cargo.cargo_max - sum_cargo)
            elif item == "lithium":
                if recipiant.cargo.lithium >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.lithium += amount
                    recipiant.cargo.lithium -= amount
                elif recipiant.cargo.lithium < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.cargo.lithium:
                    self.cargo.lithium += recipiant.cargo.lithium
                    recipiant.cargo.lithium = 0
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.cargo.lithium >= (self.cargo.cargo_max - sum_cargo):
                    self.cargo.lithium += (self.cargo.cargo_max - sum_cargo)
                    recipiant.cargo.lithium -= (self.cargo.cargo_max - sum_cargo)
            elif item == "silicon":
                if recipiant.cargo.silicon >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.silicon += amount
                    recipiant.cargo.silicon -= amount
                elif recipiant.cargo.silicon < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.cargo.silicon:
                    self.cargo.silicon += recipiant.cargo.silicon
                    recipiant.cargo.silicon = 0
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.cargo.silicon >= (self.cargo.cargo_max - sum_cargo):
                    self.cargo.silicon += (self.cargo.cargo_max - sum_cargo)
                    recipiant.cargo.silicon -= (self.cargo.cargo_max - sum_cargo)
            elif item == "people":self.cargo.cargo_max - sum_cargo) >= amount:
                    self.cargo.people += amount
                    recipiant.cargo.people -= amount
                elif recipiant.cargo.people < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.cargo.people:
                    self.cargo.people += recipiant.cargo.people
                    recipiant.cargo.people = 0
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.cargo.people >= (self.cargo.cargo_max - sum_cargo):
                    self.cargo.people += (self.cargo.cargo_max - sum_cargo)
                    recipiant.cargo.people -= (self.cargo.cargo_max - sum_cargo)
            elif item == "fuel":
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
    
    def execute(self, action):
        if action in self.waypoint.actions:
            for ship in self.ships:
                ship.waypoint = self.waypoints[1]
            if action == "unload" and self.waypoint.recipiant.x == self.x and self.waypoint.recipiant.y == self.y and self.waypoint.recipiant.z == self.z:
                self.unload()
            if action == "load" and self.waypoint.recipiant.x == self.x and self.waypoint.recipiant.y == self.y and self.waypoint.recipiant.z == self.z:
                self.unload()
            

""" Ordered list of fleet preactions for use by the Game.generate_turn """
Fleet.preactions = [
    'pre_unload',
    'pre_load',
    'piracy',
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
    'transfer',
    'buy',
    'load',
    'patrol',
    'route',
]
