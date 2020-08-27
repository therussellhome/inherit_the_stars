import sys
from .engine import Engine
from .cargo import Cargo
from . import game_engine
from random import randint
from .location import Location
from .battle_plan import BattlePlan
from .ship_design import ShipDesign
from . import stars_math

""" Default values (default, min, max)  """
__defaults = {
    'location': [Location()],
    'battle_plan': [BattlePlan()],
    'initative': [0, 0, sys.maxsize],
    'armor': [10, 0, sys.maxsize],
    'shields': [0, 0, sys.maxsize],
    'max_distance': [0.0, 0.0, sys.maxsize],
    'damage_points': [0, 0, sys.maxsize],
    'repair_points': [0, 0, sys.maxsize],
    'fuel': [0, 0, sys.maxsize],
    'fuel_max': [0, 0, sys.maxsize],
    'engines': [[]],
    'cargo': [Cargo()]
}


class Ship(ShipDesign):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    """ Moves on the ship level """
    """ If it has no engines it does an early exit with the empty return """
    def move(self, speed):
        if len(self.engines) == 0:
            return
        distance = round((((self.x - self.waypoint.x) **2) + ((self.y - self.waypoint.y) **2) + ((self.z - self.waypoint.z) **2))**.5)    
        self.x = self.x + ((speed**2)/distance)
        self.y = self.y + ((speed**2)/distance)
        self.z = self.z + ((speed**2)/distance)
    
    """ Calculates how much fuel it will take to move """
    """ Coded for use of the fleet """
    """ If there are no engines it returns 0 because it doesn't use any fuel """
    def fuel_check(self, speed, num_denials, distance):
        if len(self.engines) == 0:
            return 0
        fuel = 0
        mass_per_engine = self.mass/len(self.engines)
        for engine in self.engines:
            fuel += engine.fuel_calc(speed, mass_per_engine, num_denials, distance)
        return fuel
    
    """ Calculates how much fuel it will take to move """
    """ Coded for use of the fleet """
    """ If there are no engines it returns 0 because it doesn't use any fuel """
    def burn_fuel(self, speed, num_denials, distance, x, y, z):
        fuel = self.fuel_check(speed, num_denials, distance)
        self.location.x = x
        self.location.y = y
        self.location.z = z
        return fuel
    
    """ checks if speed will damage ship """
    def speed_is_damaging(self, speed, num_denials):
        if len(self.engines) == 0:
            return True
        mass_per_engine = self.mass/len(self.engines)
        for engine in self.engines:
            if engine.tachometer(speed, mass_per_engine, num_denials) >= 100:
                return True
        return False
    
    def colonize(self, player, planet):
        planet.colonize(player, copy.copy(player.colonize_minister), self.cargo, self.num_col_modules, self.num_col_modules, self.num_col_modules)
    
    def scan(self, player):
        pass
    
    def lay_mines(self, player, system):
        pass
    
    def open_repair_bays(self):
        return self.repair_bay_repair_points
    
    def deploy_hyper_denial(self, player):
        pass
    
    def scrap(self, location):
        #scrap algorithem
        #t = self.cost.titatium * scrap_factor
        #l = self.cost.lithium * scrap_factor
        #s = self.cost.silicon * scrap_factor
        Cargo = Cargo(titanium = t, lithium = l, silicon = s, cargo_makx = (t + l + s))
        if location not in game_engine.get('Planet/'):
            game_engine.create_salvage(copy.copy(location), Cargo)
        else:
            location.on_surface += cargo + Cargo
    
    """ Mines the planet if it is not colonized """
    def orbital_mining(self, planet):
        if planet.colonized == False:
            ti = planet.titanium - (self.rate * planet.titanium)
            si = planet.silicon - (self.rate * planet.silicon)
            li = planet.lithium - (self.rate * planet.lithium)
            planet.on_surface.titanium += round((planet.titanium - ti) + .1)
            planet.on_surface.silicon += round((planet.silicon - si) + .1)
            planet.on_surface.lithium += round((planet.lithium - li) + .1)
            planet.titanium = ti
            planet.silicon = si
            planet.lithium = li
        return planet
    
    """ Repairs the ship if it needs it """
    def repair(self, amount):
        if self.damage_points > 0:
            self.damage_points -= amount
    
    def self_repair(self):
        self.repair(self.repair_points)
    
    """ Bombs the planet if the planet is colonized """
    def bomb(self, p):
        if p.colonized == True:
            if self.bomb.percent_pop_kill * p.num_colonists < self.bomb.minimum_kill:
                p.num_colonist -= self.bomb.minimum_kill
            else:
                p.num_colonists *= self.bomb.percent_pop_kill
            p.num_facilities -= self.bomb.percent_facilities_kill
            if p.num_colonists < 0:
                p.num_colonists = 0
            if p.num_facilities < 0:
                p.num_facilities = 0
        return p

    def calc_aparent_mass(self):
        return 100

    def blow_up(self):
        pass

    def calc_initative(self):
        self.initative = 1

Ship.set_defaults(Ship, __defaults)
