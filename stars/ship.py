import copy
import sys
from random import randint
from . import stars_math
from . import game_engine
from .cargo import Cargo
from .defaults import get_default
from .engine import Engine
from .scanner import Scanner
from .location import Location
from .reference import Reference
from .ship_design import ShipDesign
from .hyperdenial import HyperDenial

""" Default values (default, min, max)  """
__defaults = {
    'commissioning': 0.0,
    'crew': Reference('Race'),
    'battle_experience': 0.0, # From surviving battle
    'navigation_experience': 0.0, # From survivng overgating
    'location': Location(),
    'fuel': (0, 0, sys.maxsize),
    'cargo': Cargo(),
    'under_construction': False,
    'armor_damage': 0,
}

""" All methods of ship are called through fleet, except maybe scan """
class Ship(ShipDesign):
    """ Initialize the cache """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__cache__['player'] = Reference('Player')
        self.__cache__['mass'] = 0
        self.__cache__['mass_per_engine'] = 0
        self.__cache__['shield_damage'] = 0
        self.__cache__['initiative'] = 0
        self.__cache__['apparent_mass'] = 0
        self.__cache__['apparent_ke'] = 0
        game_engine.register(self)

    """ Build a 'fictional' ship representing an entire fleet, used by fleet """
    def init_from(self, ships):
        super().init_from(ships)
        for key in ['fuel', 'cargo', 'armor_damage']:
            self[key] = get_default(self, key)
            for s in ships:
                self[key] += s[key]

    """ Precompute a number of values """
    def update_cache(self, player):
        self.__cache__['player'] = player
        self.__cache__['mass'] = self.mass
        if not self.crew.lrt_Trader:
            self.__cache__['mass'] += self.cargo.sum()
        if len(self.engines) > 0:
            self.__cache__['mass_per_engine'] = self.__cache__['mass'] / len(self.engines)
        self.__cache__['initiative'] = 0 #TODO age, battles, mass_per_engine, scanners, stealth, ecm
        self.__cache__['apparent_mass'] = self.__cache__['mass'] * (1 - self.cloak.percent / 100)
        if self.crew.primary_race_trait == 'Kender':
            self.__cache__['apparent_mass'] -= 25
        self.__cache__['apparent_ke'] = 0
        self.__cache__['experience'] = float(self.__cache__['player'].date) - self.__cache__['player'].race.start_date + self.battle_experience + self.navigation_experience

    """ This is a space station if it has orbital slots """
    def is_space_station(self):
        return self.hull.slots_orbital > 0

    """ Take damage """
    def take_damage(self, shield, armor):
        self.__cache__['shield_damage'] += shield
        self.armor_damage += armor
        #TODO blow-up

    """ Creates a salvage at a location """
    def create_salvage(self, location, cargo):
        return #TODO
    
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
            report['Mass'] = self.__cache__['mass']
        if scan_type != 'hyperdenial':
            report['Apparent Mass'] = self.__cache__['apparent_mass']
        return report

    """ Find owning fleet """
    def find_fleet(self):
        for f in self.__cache__['player'].fleets:
            if self in f.ships:
                return f
        return Fleet()

    """ Recompute self from components """
    def compute_stats(self, tech_level):
        if tech_level > self.level:
            self.level = tech_level
        super().compute_stats(self.level)

Ship.set_defaults(Ship, __defaults)
