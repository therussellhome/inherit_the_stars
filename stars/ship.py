import copy
import sys
from random import randint
from . import stars_math
from . import game_engine
from .asteroid import Asteroid
from .cargo import Cargo
from .defaults import get_default
from .engine import Engine
from .location import Location
from .minerals import Minerals
from .reference import Reference
from .scanner import Scanner
from .ship_design import ShipDesign

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
        self.__cache__['total_mass'] = 0
        self.__cache__['mass_per_engine'] = 0
        self.__cache__['shield_damage'] = 0
        self.__cache__['initiative'] = 0
        self.__cache__['apparent_mass'] = 0
        self.__cache__['apparent_ke'] = 0
        if 'from_ships' in kwargs:
            for s in kwargs['from_ships']:
                self.merge(s)
                for key in ['fuel', 'cargo', 'armor_damage']:
                    self[key] += s[key]
        else:
            game_engine.register(self)

    """ Precompute a number of values """
    def update_cache(self, player):
        self.__cache__['player'] = player
        self.__cache__['total_mass'] = self.mass
        if not self.crew.lrt_Trader:
            self.__cache__['total_mass'] += self.cargo.sum()
        else:
            self.__cache__['total_mass'] += self.cargo.people
        if len(self.engines) > 0:
            self.__cache__['mass_per_engine'] = self.__cache__['total_mass'] / len(self.engines)
        self.__cache__['apparent_mass'] = self.__cache__['total_mass'] * (1 - self.cloak.percent / 100)
        if self.crew.primary_race_trait == 'Kender':
            self.__cache__['apparent_mass'] -= 25
        self.__cache__['apparent_ke'] = 0
        self.__cache__['experience'] = 1 + float(self.__cache__['player'].date) - self.__cache__['player'].race.start_date + self.battle_experience + self.navigation_experience
        self.__cache__['initiative'] = self.__cache__['experience'] #TODO add mass_per_engine, scanners, stealth, ecm

    """ This is a space station if it has orbital slots """
    def is_space_station(self):
        return self.hull.slots_orbital > 0

    """ Take damage """
    def take_damage(self, shield, armor):
        self.__cache__['shield_damage'] += shield
        self.armor_damage += armor
        if self.armor_damage >= self.armor:
            self.scrap(True)
            # TODO remove from fleet

    """ Scrap/blow-up the ship """
    def scrap(self, destroyed=False):
        if destroyed:
            if randint(0, 1) == 0:
                return
            scrap_value = Minerals() + self.cargo + self.cost * 0.5
        else:
            scrap_value = Minerals() + self.cargo + self.cost * (self.__cache__['player'].race.scrap_rate() / 100)
            scrap_value += self.cargo
        if self.location.reference ^ 'Planet':
            self.location.reference.on_surface += scrap_value
        else:
            self.__cache__['player'].game.asteroids.append(Asteroid(minerals=scrap_value, location=Location(self.location.xyz)))

    """ Calculate the scrap value """
    def scrap_value(self):
        # Force scrap to be just minerals, cost already accounts for miniaturization
        m = Minerals() + self.cost
        return m * (self.__cache__['player'].race.scrap_rate() / 100)

    """ Return the apparent kinetic energy """
    def calc_apparent_ke(self):
        return self.__cache__.get('apparent_ke', 0)

    """ Return intel report when scanned """
    def scan_report(self, scan_type=''):
        report = {
            'location': self.location,
        }
        if scan_type == 'anticloak':
            report['Mass'] = self.__cache__['total_mass'] #TODO use ke instead of mass?
        if scan_type != 'hyperdenial':
            report['Apparent Mass'] = self.__cache__['apparent_mass']
        return report

    """ Find owning fleet """
    def find_fleet(self):
        for f in self.__cache__['player'].fleets:
            if self in f.ships:
                return f
        return Fleet()

Ship.set_defaults(Ship, __defaults)
