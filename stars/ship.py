import copy
import sys
from random import random, randint
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
    'armor_damage': (0, 0, sys.maxsize),
}

""" Temporary values (default, min, max)  """
__tmp_defaults = {
    'player': Reference('Player'),
    'fleet': Reference('Fleet'),
    'hyper': 0,
    'shield_damage': 0,
    'initiative': None,
    'total_mass': None,
    'apparent_mass': None,
    'mass_per_engine': None,
    'ke': None,
    'apparent_ke': None,
}

""" All methods of ship are called through fleet, except maybe scan """
class Ship(ShipDesign):
    """ Initialize, if from ships this is a pseudo-ship combining the stats of other ships """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'from_ships' in kwargs:
            for s in kwargs['from_ships']:
                self.merge(s, max_not_merge=True)
                for key in ['fuel', 'cargo', 'armor_damage']:
                    self[key] += s[key]
        else:
            game_engine.register(self)

    """ Provide calculated values """
    def __getattribute__(self, name):
        self_dict = object.__getattribute__(self, '__dict__')
        # Safety check if inital defaults have not been applied or if has value
        if '__init_complete__' not in self_dict or name not in self_dict or self_dict[name] is not None:
            return super().__getattribute__(name)
        # Calculate if not yet calculated
        if name == 'initiative':
            self_dict[name] = 1 + float(self.player.date) - self.player.race.start_date + self.battle_experience + self.navigation_experience #TODO add 1/mass_per_engine, scanners, stealth, ecm
        elif name == 'total_mass':
            self_dict[name] = self.mass
            if not self.crew.lrt_Trader:
                self_dict[name] += self.cargo.sum()
            else:
                self_dict[name] += self.cargo.people
        elif name == 'apparent_mass':
            self_dict[name] = self.total_mass * (100.0 - self.cloak.percent) / 100.0
            if self.crew.primary_race_trait == 'Kender':
                self_dict[name] -= 25
        elif name == 'mass_per_engine':
            if len(self.engines) > 0:
                self_dict[name] = self.total_mass / len(self.engines)
        elif name == 'ke':
            self_dict[name] = self.total_mass * self.hyper * self.hyper
        elif name == 'apparent_ke':
            self_dict[name] = self.apparent_mass * self.hyper * self.hyper
        return super().__getattribute__(name)

    """ Reset time based values"""
    def next_hundreth(self):
        self.hyper = 0
        self.shield_damage = 0
        self.initiative = None
        self.ke = None
        self.apparent_ke = None

    """ Force recalc of mass """
    def update_cargo(self):
        self.total_mass = None
        self.apparent_mass = None
        self.mass_per_engine = None
        self.ke = None
        self.apparent_ke = None

    """ Travel through a stargate and incur any overgate damage/experience """
    def gate(self, distance, gate_strength, survival_test=False):
        over = self.total_mass + distance - gate_strength
        if over <= 0:
            return True
        modifier = 512
        if self.crew.primary_race_trait == 'Patryns':
            modifier = 256 # TODO is this a good number?
        min_damage = round((over/gate_strength + over/1000.0)**1.3 * modifier)
        if survival_test:
            print(min_damage, self.armor, self.armor_damage)
            return min_damage < (self.armor - self.armor_damage)
        luck = random() * 5/self.initiative
        self.navigation_experience += 1
        return not self.take_damage(0, min_damage * (1 + luck))

    """ Take damage """
    def take_damage(self, shield, armor):
        self.shield_damage += shield
        self.armor_damage += armor
        if self.armor_damage >= self.armor:
            self.scrap(randint(0, 100))
            self.fleet.remove_ships(self)
            self.player.remove_ships(self)
            return True
        return False

    """ Scrap/blow-up the ship """
    def scrap(self, percent_destroyed=None):
        scrap_value = Minerals() + self.cargo + self.cost * self.player.race.scrap_rate / 100.0
        if percent_destroyed:
            scrap_value *= 1.0 - percent_destroyed / 100.0
        if self.location.reference ^ 'Planet':
            self.location.reference.on_surface += scrap_value
        elif not scrap_value.is_zero():
           self.player.game.asteroids.append(Asteroid(minerals=scrap_value, location=Location(self.location.xyz)))
        return scrap_value

    """ Return intel report when scanned """
    def scan_report(self, scan_type=''):
        report = {
            'location': self.location,
        }
        if scan_type == 'anticloak':
            report['Mass'] = self.total_mass
        elif scan_type == 'penetrating':
            report['Apparent Mass'] = self.apparent_mass
        elif scan_type == 'normal':
            report['Apparent KE'] = self.apparent_ke
        return report

Ship.set_defaults(Ship, __defaults, __tmp_defaults)
