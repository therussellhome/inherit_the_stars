import sys
import copy
from . import stars_math
from . import game_engine
from .cargo import Cargo
from random import randint
from .engine import Engine
from .scanner import Scanner
from .location import Location
from .expirence import Expirence
from .reference import Reference
from .battle_plan import BattlePlan
from .ship_design import ShipDesign
from .hyperdenial import HyperDenial

""" Default values (default, min, max)  """
__defaults = {
    'location': Location(),
    'battle_plan': BattlePlan(),
    'initative': (0, 0, sys.maxsize),
    'armor': (10, 0, sys.maxsize),
    'armor_damage': (0, 0, sys.maxsize),
    'shields': (0, 0, sys.maxsize),
    'shields_damage': (0, 0, sys.maxsize),
    'max_distance': (0.0, 0.0, sys.maxsize),
    'damage_armor': (0, 0, sys.maxsize),
    'fuel': (0, 0, sys.maxsize),
    'fuel_max': (0, 0, sys.maxsize),
    'engines': [],
    'cargo': Cargo(),
    'expirence': Expirence(),
    'player': Reference('Player'),
}

""" All methods of ship are called through fleet, except maybe scan """
class Ship(ShipDesign):
    """ Calculates how much fuel it will take to move """
    """ If there are no engines it returns 0 because it doesn't use any fuel """
    def fuel_check(self, speed, num_denials, distance):
        if len(self.engines) == 0:
            return 0
        fuel = 0
        mass_per_engine = self.calc_mass()/len(self.engines)
        for engine in self.engines:
            fuel += engine.fuel_calc(speed, mass_per_engine, num_denials, distance)
        return fuel
    
    """ Calculates how much fuel it will take to move """
    """ If there are no engines it returns 0 because it doesn't use any fuel """
    def move(self, speed, num_denials, distance):
        self.__cache__['apparent_ke'] = self.calc_apparent_mass() * pow(speed, 4)
        damage = 0
        if len(self.engines) == 0:
            damage = sys.maxsize
            return 0
        mass_per_engine = self.calc_mass()/len(self.engines)
        for engine in self.engines:
            damage += engine.damage_calc(speed, mass_per_engine, distance, num_denials)
            #TODO do something with the damage number
        return self.fuel_check(speed, num_denials, distance)
    
    """ Checks if speed will damage ship, returns True if speed will damage ship """
    def speed_is_damaging(self, speed, num_denials):
        if len(self.engines) == 0:
            return None
        mass_per_engine = self.calc_mass()/len(self.engines)
        for engine in self.engines:
            if engine.tachometer(speed, mass_per_engine, num_denials) >= 100:
                return True
        return False
    
    """ Tells the planet that it has been colonized and unloads and sraps the ship """
    def colonize(self, player, planet):
        planet.colonize(player)
        planet.on_surface += self.cargo
        for attr in ['titanium', 'people', 'lithium', 'silicon']:
            self.cargo[attr] = 0
        self.scrap(planet, self.location, 0.95)
    
    
    """ Lays mines """
    def lay_mines(self, player, system):
        return#TODO system.mines[player.name] += self.mines_laid
    
    """ Returns the repair value of the repair bay """
    def open_repair_bays(self):
        return self.repair_bay
    
    """ Recurns the self repair value """
    def damage_control(self):
        return self.repair
    
    """ Creates a hyper denial object """
    def deploy_hyper_denial(self, player):
        self.hyper_denial.on = True
    
    """ Creates a salvage at a location """
    def create_salvage(self, location, cargo):
        return#TODO
    
    """ Scraps the ship """
    def scrap(self, planet, location, scrap_factor = 0.9):
        t = round(self.cost.titanium * scrap_factor)
        l = round(self.cost.lithium * scrap_factor)
        s = round(self.cost.silicon * scrap_factor)
        cargoo = Cargo(titanium = t, lithium = l, silicon = s, cargo_max = (t + l + s))
        if planet not in game_engine.get('Planet'):
            self.create_salvage(copy.copy(location), cargoo + self.cargo)
        else:
            planet.on_surface += cargoo + self.cargo
    
    """ Mines the planet if the planet is not colonized """
    def orbital_mining(self, planet):
        if not planet.is_colonized():
            planet.on_surface.titanium += round(self.mining_rate * planet.mineral_availability('titanium'))
            planet.on_surface.silicon += round(self.mining_rate * planet.mineral_availability('silicon'))
            planet.on_surface.lithium += round(self.mining_rate * planet.mineral_availability('lithium'))
            planet.remaining_minerals.titanium -= round(self.mining_rate * planet.mineral_availability('titanium') * self.percent_wasted)
            planet.remaining_minerals.silicon -= round(self.mining_rate * planet.mineral_availability('silicon') * self.percent_wasted)
            planet.remaining_minerals.lithium -= round(self.mining_rate * planet.mineral_availability('lithium') * self.percent_wasted)
    
    """ Repairs the ship if it needs it """
    def repair_self(self, amount):
        max_armor = self.max_armor()
        if (max_armor - self.armor) > 0:
            self.armor += min((max_armor - self.armor), amount)
            return amount - min((max_armor - self.armor), amount)
    
    """ Returns the number of facilities and amount of population that is killed """
    def bomb(self, planet, shields, pop):
        facility_kill = 0
        pop_kill = 0
        for bomb in self.bombs:
            facility_kill += bomb.kill_shield_facilities(pop, shields)
            pop_kill += bomb.kill_population(pop, shields)
        return facility_kill, pop_kill
    
    """ Does the ship have any cloak that would show up on anti-cloak scanners """
    def has_cloaked(self):
        if self.race.primary_race_trait == 'Kender' or self.cloak.percent > 0:
            return True
        return False
    
    """ Adjust the mass for cloaking """
    def calc_apparent_mass(self):
        if self.race.primary_race_trait == 'Kender':
            return self.calc_mass() * (1 - self.cloak.percent / 100) - 25
        return self.calc_mass() * (1 - self.cloak.percent / 100)
    
    """ Returns the actual mass of the ship, excluding cargo if the ship was made by a trader race """
    def calc_mass(self):
        mass = self.mass + self.cargo.silicon + self.cargo.titanium + self.cargo.lithium
        #TODO check if crew is trader
        #if self.player.is_valid and self.race.lrt_trader:
        #    mass = self.mass
        return mass + self.cargo.people
    
    """ Executes the on_destruction sequence """
    def blow_up(self):
        return#TODO self.scrap(self.location, self.location)

    """ Return the apparent kinetic energy """
    def calc_apparent_ke(self):
        return self.__cache__.get('apparent_ke', 0)

    """ Return intel report when scanned """
    def scan_report(self, scan_type=''):
        report = {
            'location': self.location,
        }
        if scan_type == 'anticloak':
            report['Mass'] = obj.calc_mass()
        if scan_type != 'hyperdenial':
            report['Apparent Mass'] = self.calc_apparent_mass()
        return report

Ship.set_defaults(Ship, __defaults)
