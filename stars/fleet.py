import sys
from . import stars_math
from . import game_engine
from .ship import Ship
from .cargo import Cargo
from .player import Player
from .planet import Planet
from .defaults import Defaults
from .location import Location
from .waypoint import Waypoint
from .location import LocationReference
from .reference import Reference


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
    'cargo': [Cargo()]
}


""" Class defining fleets - directly modifiable by the player """
class Fleet(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        self.ships = []
        if 'ships' in kwargs:
            ships = kwargs['ships']
            while len(ships) > 0:
                ship = ships[0]
                self.add_ship(ship)
                ships.remove(ship)
            del kwargs['ships']
        super().__init__(**kwargs)
        self.player.fleets.append(self)
        self.name = 'Fleet #'+str(hex(id(self)))[-7:-1]
        self.compile()
        self.returnn()
    
    """ adds the ships to self.ships """
    def add_ship(self, ship):
        if len(self.ships) == 0:
            self.location = Location(x=ship.location.x, y=ship.location.y, z=ship.location.z)
            self.ships.append(ship)
        else:
            if (self.location - ship.location) > (stars_math.TERAMETER_2_LIGHTYEAR * 2):
                return
            else:
                self.ships.append(ship)
    
    '''""" finds the largest range of hyper denial had by a ship in the fleet and asigns the fleet that value """
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
    
    """ calculates the scaning of the fleet from curent position """
    def calculate_scanning(self):
        for ship in self.ships:
            ship.scan()
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
                distance = self.location.__sub__(planet.location)
                if distance <= self.pennetrating_scanner:
                    self.player.create_intel_on(planet, "planet")
                    if distance <= self.anti_cloak_scanner:
                        self.player.create_intel_on(planet.space_station, planet.space_station.mass, True)
                    elif planet.space_station.aparant_mass > 0:
                        self.player.create_intel_on(planet.space_station, planet.space_station.aparant_mass)'''
    
    """ checks if can upgrade and then stops moving if comanded to """
    def check_upgrade(self):
        self.waypoints[1] = waypoint
        if waypoint.upgrade_if_commanded == True and self.waypoints[1].location in game_engine.get('Planets/') and self.waypoints[1].location.space_station:
            for ship in self.ships:
                if ship.new_design and ship.new_design.mass <= self.waypoints[1].location.space_station.max_build_mass:
                    self.waypoints[1].location.upgrade(ship)
    
    """ takes the move distance and changes self.location accordingly """
    def calc_move(self, location, amount):
        dis, x, y, z = self.calc_distance(location)
        a = ((amount)**2)**(1/2)
        mod_x = (self.location.x-location.x)/x
        mod_y = (self.location.y-location.y)/y
        mod_z = (self.location.z-location.z)/z
        self.location.x -= mod_x*(x/dis)*a
        self.location.y -= mod_y*(y/dis)*a
        self.location.z -= mod_z*(z/dis)*a
    
    """ checks the distance between the fleet an the fly_to point """
    def calc_distance(self, location):
        dis_x = ((self.location.x-location.x)**2)**(1/2)
        dis_y = ((self.location.y-location.y)**2)**(1/2)
        dis_z = ((self.location.z-location.z)**2)**(1/2)
        distance = ((dis_x)**2 + (dis_y)**2 + (dis_z)**2)**(1/2)
        return distance, dis_x, dis_y, dis_z
    
    """ does all the moving calculations and then moves the ships """
    def move(self, time_in):
        self.waypoints[1].move_to(self, time_in)
        in_hyper_denial = False
        num_denials = 0
        for ship in self.ships:
            self.fuel += ship.fuel
            #if 
        for hyper_denial in game_engine.hyper_denials:
            distance_to_denial = self.location - hyper_denial.location
            if distance_to_denial >= hyper_denial.range and hyper_denial.player:
                num_denials += 1
        speed = waypoints[1].speed
        distance_to_waypoint = self.location - self.waypoints[1].fly_to
        distance_at_hyper = (speed**2)/100
        if distance_to_waypoint < distance_at_hyper:
            distance = distance_to_waypoint
        else:
            distance = distance_at_hyper
        if distance_to_waypoint == 0:
            if self.waypoints[1].move_on == True:
                self.waypoints.pop(0)
                self.move(time_in)
        while self.test_fuel(speed, in_hyper_denial, distance):
            speed -= 1
            distance_at_hyper = (speed**2)/100
            if distance_to_waypoint < distance_at_hyper:
                distance = distance_to_waypoint
            else:
                distance = distance_at_hyper
        self.calc_move(self.waypoints[1].fly_to, distance)
        self.burn_fuel(speed, in_hyper_denial, distance)
        self.returnn()
    
    """ calles the move for each of the ships """
    def burn_fuel(self, speed, num_denials, dis):
        fuel_1_ly = 0
        for ship in self.ships:
            fuel_1_ly += ship.burn_fuel(speed, num_denials, dis, self.location.x, self.location.y, self.location.z)
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
    
    """ makes a hyper_denial """
    def deploy_hyper_denial(self):
        hyper_denial = False
        for ship in self.ships:
            if ship.hyper_denial == True:
                ship.deploy_hyper_denial()
                hyper_denial = True
        if not hyper_denial:
            pass
            
    
    """ Merges the fleet with the target fleet """
    def merge(self):
        self.compile()
        self.waypoints[0].recipiants['merge'].compile()
        for ship in self.ships:
            self.waypoints[0].recipiants['merge'].ships.append(ship)
        self.ships = []
        self.waypoints[0].recipiants['merge'].fuel += self.fuel
        self.fuel = 0
        self.waypoints[0].recipiants['merge'].cargo.titanium += self.cargo.titanium
        self.cargo.titanium = 0
        self.waypoints[0].recipiants['merge'].cargo.lithium += self.cargo.lithium
        self.cargo.lithium = 0
        self.waypoints[0].recipiants['merge'].cargo.silicon += self.cargo.silicon
        self.cargo.silicon = 0
        self.waypoints[0].recipiants['merge'].cargo.people += self.cargo.people
        self.cargo.people = 0
        self.waypoints[0].recipiants['merge'].returnn()
    
    """ splits the fleet """
    def split(self, splits, name=None):
        ships = []
        for split in splits:
            ships.append(self.ships[split])
        for ship in ships:
            self.ships.remove(ship)
        #fleet = Fleet('ships'=ships, 'name'=name)
        #self.player.fleets.append(fleet)
    
    """ executes the unload function """
    def unload(self, recipiant):
        if recipiant not in self.player.fleets:
            return
        self.compile()
        recipiant.compile()
        for transfer in self.waypoints[0].transfers['unload']:
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
        recipiant.returnn()
    
    """ executes the sell function """
    def sell(self, recipiant):
        self.compile()
        for transfer in self.waypoints[0].transfers['sell']:
            item = transfer[0]
            amount = transfer[1]
            traety = self.player.treaties[recipiant.player.name].sell
            if item == 'titanium' and traety.cost_titanium != None:
                if self.cargo.titanium >= amount:
                    if recipiant.player.energy < (amount * traety.cost_titanium):
                        amount = int(recipiant.player.energy / traety.cost_titanium)
                    self.cargo.titanium -= amount
                    recipiant.on_surface.titanium += amount
                    self.player.energy += (amount * traety.cost_titanium)
                    recipiant.player.energy -= (amount * traety.cost_titanium)
                else:
                    amount = self.cargo.titanium
                    if recipiant.player.energy < (amount * traety.cost_titanium):
                        amount = int(recipiant.player.energy / traety.cost_titanium)
                    self.cargo.titanium -= amount
                    recipiant.on_surface.titanium += amount
                    self.player.energy += (amount * traety.cost_titanium)
                    recipiant.player.energy -= (amount * traety.cost_titanium)
            elif item == 'lithium' and traety.cost_lithium != None:
                if self.cargo.lithium >= amount:
                    if recipiant.player.energy < (amount * traety.cost_lithium):
                        amount = int(recipiant.player.energy / traety.cost_lithium)
                    self.cargo.lithium -= amount
                    recipiant.on_surface.lithium += amount
                    self.player.energy += (amount * traety.cost_lithium)
                    recipiant.player.energy -= (amount * traety.cost_lithium)
                else:
                    amount = self.cargo.lithium
                    if recipiant.player.energy < (amount * traety.cost_lithium):
                        amount = int(recipiant.player.energy / traety.cost_lithium)
                    self.cargo.lithium -= amount
                    recipiant.on_surface.lithium += amount
                    self.player.energy += (amount * traety.cost_lithium)
                    recipiant.player.energy -= (amount * traety.cost_lithium)
            elif item == 'silicon' and traety.cost_silicon != None:
                if self.cargo.silicon >= amount:
                    if recipiant.player.energy < (amount * traety.cost_silicon):
                        amount = int(recipiant.player.energy / traety.cost_silicon)
                    self.cargo.silicon -= amount
                    recipiant.on_surface.silicon += amount
                    self.player.energy += (amount * traety.cost_silicon)
                    recipiant.player.energy -= (amount * traety.cost_silicon)
                else:
                    amount = self.cargo.silicon
                    if recipiant.player.energy < (amount * traety.cost_silicon):
                        amount = int(recipiant.player.energy / traety.cost_silicon)
                    self.cargo.silicon -= amount
                    recipiant.on_surface.silicon += amount
                    self.player.energy += (amount * traety.cost_silicon)
                    recipiant.player.energy -= (amount * traety.cost_silicon)
            elif item == 'fuel' and traety.cost_fuel != None:
                if self.fuel >= amount and (recipiant.space_station.fuel_max - recipiant.space_station.fuel) >= amount:
                    if recipiant.player.energy < (amount * traety.cost_fuel):
                        amount = int(recipiant.player.energy / traety.cost_fuel)
                    self.fuel -= amount
                    recipiant.space_station.fuel += amount
                    self.player.energy += (amount * traety.cost_fuel)
                    recipiant.player.energy -= (amount * traety.cost_fuel)
                elif self.fuel < amount and (recipiant.space_station.fuel_max - recipiant.space_station.fuel) >= self.fuel:
                    amount = self.fuel
                    if recipiant.player.energy < (amount * traety.cost_fuel):
                        amount = int(recipiant.player.energy / traety.cost_fuel)
                    self.fuel -= amount
                    recipiant.spase_station.fuel += amount
                    self.player.energy += (amount * traety.cost_fuel)
                    recipiant.player.energy -= (amount * straety.cost_fuel)
                elif (recipiant.spase_station.fuel_max - recipiant.spase_station.fuel) < amount and self.fuel >= (recipiant.spase_station.fuel_max - recipiant.spase_station.fuel):
                    amount = (recipiant.fuel_max - recipiant.fuel)
                    if recipiant.player.energy < (amount * traety.cost_fuel):
                        amount = int(recipiant.player.energy / traety.cost_fuel)
                    self.fuel -= amount
                    recipiant.spase_station.fuel += amount
                    self.player.energy += (amount * traety.cost_fuel)
                    recipiant.player.energy -= (amount * traety.cost_fuel)
        self.returnn()
    
    """ executes the buy function """
    def buy(self, recipiant):
        self.compile()
        for transfer in self.waypoints[0].transfers['buy']:
            item = transfer[0]
            amount = transfer[1]
            sum_cargo = (self.cargo.titanium + self.cargo.lithium + self.cargo.silicon + self.cargo.people)
            traety = self.player.treaties[recipiant.player.name].buy
            if item == 'titanium' and traety.cost_titanium != None:
                if recipiant.on_surface.titanium >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    if self.player.energy < (amount * traety.cost_titanium):
                        amount = int(self.player.energy / traety.cost_titanium)
                    recipiant.on_surface.titanium -= amount
                    self.cargo.titinium += amount
                    self.player.energy -= (amount * traety.cost_titanium)
                    recipiant.player.energy += (amount * traety.cost_titanium)
                elif recipiant.on_surface.titanium < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.on_surface.titanium:
                    amount = recipiant.on_surface.titanium
                    if self.player.energy < (amount * traety.cost_titanium):
                        amount = int(self.player.energy / traety.cost_titanium)
                    recipiant.cargo.titanium -= amount
                    self.cargo.titinium += amount
                    self.player.energy -= (amount * traety.cost_titanium)
                    recipiant.player.energy += (amount * traety.cost_titanium)
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.on_surface.titanium >= (self.cargo.cargo_max - sum_cargo):
                    amount = (self.cargo.cargo_max - sum_cargo)
                    if self.player.energy < (amount * traety.cost_titanium):
                        amount = int(self.player.energy / traety.cost_titanium)
                    recipiant.on_surface.titanium -= amount
                    self.cargo.titinium += amount
                    self.player.energy -= (amount * traety.cost_titanium)
                    recipiant.player.energy += (amount * traety.cost_titanium)
            elif item == 'lithium' and traety.cost_lithium != None:
                if recipiant.on_surface.lithium >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    if self.player.energy < (amount * traety.cost_lithium):
                        amount = int(self.player.energy / traety.cost_lithium)
                    self.cargo.lithium += amount
                    recipiant.on_surface.lithium -= amount
                    self.player.energy -= (amount * traety.cost_lithium)
                    recipiant.player.energy += (amount * traety.cost_lithium)
                elif recipiant.on_surface.lithium < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.on_surface.lithium:
                    amount = recipiant.on_surface.lithium
                    if self.player.energy < (amount * traety.cost_lithium):
                        amount = int(self.player.energy / traety.cost_lithium)
                    self.cargo.lithium += amount
                    recipiant.on_surface.lithium -= amount
                    self.player.energy -= (amount * traety.cost_lithium)
                    recipiant.player.energy += (amount * traety.cost_lithium)
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.on_surface.lithium >= (self.cargo.cargo_max - sum_cargo):
                    amount = (self.cargo.cargo_max - sum_cargo)
                    if self.player.energy < (amount * traety.cost_lithium):
                        amount = int(self.player.energy / traety.cost_lithium)
                    self.cargo.lithium += amount
                    recipiant.on_surface.lithium -= amount
                    self.player.energy -= (amount * traety.cost_lithium)
                    recipiant.player.energy += (amount * traety.cost_lithium)
            elif item == 'silicon' and traety.cost_silicon != None:
                if recipiant.on_surface.silicon >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    if self.player.energy < (amount * traety.cost_silicon):
                        amount = int(self.player.energy / traety.cost_silicon)
                    self.cargo.silicon += amount
                    recipiant.on_surface.silicon -= amount
                    self.player.energy -= (amount * traety.cost_silicon)
                    recipiant.player.energy += (amount * traety.cost_silicon)
                elif recipiant.on_surface.silicon < amount and (self.cargo.cargo_max - sum_cargo) >= recipiant.on_surface.silicon:
                    amount = recipiant.on_surface.silicon
                    if self.player.energy < (amount * traety.cost_silicon):
                        amount = int(self.player.energy / traety.cost_silicon)
                    self.cargo.silicon += amount
                    recipiant.on_surface.silicon -= amount
                    self.player.energy -= (amount * traety.cost_silicon)
                    recipiant.player.energy += (amount * traety.cost_silicon)
                elif (self.cargo.cargo_max - sum_cargo) < amount and recipiant.on_surface.silicon >= (self.cargo.cargo_max - sum_cargo):
                    amount = (self.cargo.cargo_max - sum_cargo)
                    if self.player.energy < (amount * traety.cost_silicon):
                        amount = int(self.player.energy / traety.cost_silicon)
                    self.cargo.silicon += amount
                    recipiant.on_surface.silicon -= amount
                    self.player.energy -= (amount * traety.cost_silicon)
                    recipiant.player.energy += (amount * traety.cost_silicon)
            elif item == 'fuel' and traety.cost_fuel != None:
                if recipiant.space_station.fuel >= amount and (self.fuel_max - self.fuel) >= amount:
                    if self.player.energy < (amount * traety.cost_fuel):
                        amount = int(self.player.energy / traety.cost_fuel)
                    self.fuel += amount
                    recipiant.space_station.fuel -= amount
                    self.player.energy -= (amount * traety.cost_fuel)
                    recipiant.player.energy += (amount * traety.cost_fuel)
                elif recipiant.space_station.fuel < amount and (self.fuel_max - self.fuel) >= recipiant.space_station.fuel:
                    amount = recipiant.space_station.fuel
                    if self.player.energy < (amount * traety.cost_fuel):
                        amount = int(self.player.energy / traety.cost_fuel)
                    self.fuel += amount
                    recipiant.space_station.fuel -= amount
                    self.player.energy -= (amount * traety.cost_fuel)
                    recipiant.player.energy += (amount * traety.cost_fuel)
                elif (self.fuel_max - self.fuel) < amount and recipiant.space_station.fuel >= (self.fuel_max - self.fuel):
                    amount = (self.fuel_max - self.fuel)
                    if self.player.energy < (amount * traety.cost_fuel):
                        amount = int(self.player.energy / traety.cost_fuel)
                    self.fuel += amount
                    recipiant.space_station.fuel -= amount
                    self.player.energy -= (amount * traety.cost_fuel)
                    recipiant.player.energy += (amount * traety.cost_fuel)
        self.returnn()
    
    """ executes the load function """
    def load(self, recipiant):
        if recipiant not in self.player.fleets:
            return
        self.compile()
        recipiant.compile()
        for transfer in self.waypoints[0].transfers['load']:
            item = transfer[0]
            amount = transfer[1]
            sum_cargo = (self.cargo.titanium + self.cargo.lithium + self.cargo.silicon + self.cargo.people)
            if item == 'titanium':
                if recipiant.cargo.titanium >= amount and (self.cargo.cargo_max - sum_cargo) >= amount:
                    recipiant.cargo.titanium -= amount
                    self.cargo.titanium += amount
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
                if self.cargo.cargo_max - sum_cargo >= amount:
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
        recipiant.returnn()
    
    """ runs all of the actions """
    def execute(self, action):
        self.waypoint = self.waypoints[0]
        if action in self.waypoint.actions:
            if action == 'unload' or action == 'pre_unload' and (self.waypoint.location - self.location) <= (2 * stars_math.TERAMETER_2_LIGHTYEAR):
                recipiant = self.waypoint.recipiants['unload']
                if recipiant == "deep_space" or recipiant.name == 'salvage' or recipiant.player.name == self.player.name:
                    self.unload(recipiant)
            if action == 'load' or action == 'pre_load' and (self.waypoint.location - self.location) <= (2 * stars_math.TERAMETER_2_LIGHTYEAR):
                recipiant = self.waypoint.recipiants['load']
                if recipiant.name == 'salvage' or recipiant.player.name == self.player.name:
                    self.load(recipiant)
            if action == 'buy' and self.waypoint.recipiants['buy'] in game_engine.get('Planet/') and self.waypoint.recipiants['buy'].space_station.trade and (self.waypoint.location - self.location) <= (2 * stars_math.TERAMETER_2_LIGHTYEAR):
                recipiant = self.waypoint.recipiants['buy']
                if recipiant.player.name != self.player.name:
                    self.buy(recipiant)
            if action == 'sell':
                recipiant = self.waypoint.recipiants['sell']
                if recipiant in game_engine.get('Planet/') and recipiant.space_station.trade and (self.waypoint.location - self.location) <= (2 * stars_math.TERAMETER_2_LIGHTYEAR):
                    recipiant = self.waypoint.recipiants['sell']
                    if recipiant.player.name != self.player.name:
                        self.sell(recipiant)
            if action == 'deploy_hyper_denial' and self.waypoint.speed == 0:
                self.deploy_hyper_denial()
            if action == 'merge' and (self.waypoint.location - self.location) <= (2 * stars_math.TERAMETER_2_LIGHTYEAR):
                self.merge()
            
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
    'generate_fuel',
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
