import sys
from .reference import Reference
from .engine import Engine
from .cargo import Cargo
from . import game_engine
from random import randint
from .location import Location
from .battle_plan import BattlePlan
from .ship_design import ShipDesign
from . import stars_math
from .expirence import Expirence
import copy

""" Default values (default, min, max)  """
__defaults = {
    'location': [Location()],
    'battle_plan': [BattlePlan()],
    'initative': [0, 0, sys.maxsize],
    'armor': [10, 0, sys.maxsize],
    'armor_damage': [0, 0, sys.maxsize],
    'shields': [0, 0, sys.maxsize],
    'shields_damage': [0, 0, sys.maxsize],
    'max_distance': [0.0, 0.0, sys.maxsize],
    'damage_armor': [0, 0, sys.maxsize],
    'fuel': [0, 0, sys.maxsize],
    'fuel_max': [0, 0, sys.maxsize],
    'engines': [[]],
    'cargo': [Cargo()],
    'expirence': [Expirence()],
    'cloak_percent': [0.0, 0.0, 100.0],
    'player': [Reference()]
}


class Ship(ShipDesign):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
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
    
    """ TODO """
    """ Calculates how much fuel it will take to move """
    """ Coded for use of the fleet """
    """ If there are no engines it returns 0 because it doesn't use any fuel """
    def move(self, speed, num_denials, fly_to, distance):
        self.location = self.location.move(fly_to, distance)
        return self.fuel_check(speed, num_denials, distance)
    
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
        planet.colonize(player, copy.copy(player.get_minister(planet)), self.cargo.people)
        self.cargo.people = 0
    
    def scan(self, player):
        pass
    
    def lay_mines(self, player, system):
        pass
    
    def open_repair_bays(self):
        return self.repair_bay
    
    def damage_control(self):
        return self.repair
    
    def deploy_hyper_denial(self, player):
        pass
    
    def create_salvage(self, location, cargo):
        pass
    
    def scrap(self, planet, location, scrap_factor=0.9):
        t = round(self.cost.titanium * scrap_factor)
        l = round(self.cost.lithium * scrap_factor)
        s = round(self.cost.silicon * scrap_factor)
        cargoo = Cargo(titanium = t, lithium = l, silicon = s, cargo_max = (t + l + s))
        if planet not in game_engine.get('Planet'):
            self.create_salvage(copy.copy(location), cargoo + self.cargo)
        else:
            planet.on_surface += cargoo + self.cargo
    
    """ Mines the planet if it is not colonized """
    def orbital_mining(self, planet):
        if not planet.player.is_valid:
            planet.on_surface.titanium += round(self.mining_rate * planet.get_availability('titanium'))
            planet.on_surface.silicon += round(self.mining_rate * planet.get_availability('silicon'))
            planet.on_surface.lithium += round(self.mining_rate * planet.get_availability('lithium'))
            planet.remaining_minerals.titanium -= round(self.mining_rate * planet.get_availability('titanium') * self.percent_wasted)
            planet.remaining_minerals.silicon -= round(self.mining_rate * planet.get_availability('silicon') * self.percent_wasted)
            planet.remaining_minerals.lithium -= round(self.mining_rate * planet.get_availability('lithium') * self.percent_wasted)
    
    """ Repairs the ship if it needs it """
    def repair_self(self, amount):
        if self.damage_armor > 0:
            self.damage_armor -= amount
    
    """ Bombs the planet if the planet is colonized """
    def bomb(self, planet, shields, pop):
        facility_kill = 0
        pop_kill = 0
        for bomb in self.bombs:
            facility_kill += bomb.kill_shield_facilities(pop, shields)
            pop_kill += bomb.kill_population(pop, shields)
        return facility_kill, pop_kill

    def calc_apparent_mass(self):
        return self.mass * (1 - self.cloak_percent)# - self.cloak_KT

    def blow_up(self):
        self.scrap(self.location, self.location)
        pass


Ship.set_defaults(Ship, __defaults)
