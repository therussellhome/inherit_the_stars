import copy
import sys
from . import game_engine
from .cloak import Cloak
from .cost import Cost
from .defaults import Defaults
from .hyperdenial import HyperDenial
from .scanner import Scanner
from .tech_level import TechLevel


""" Default values (default, min, max)  """
__defaults = {
    'name': ['Tech the GM made up himself'],
    'category': [''],
    'slot_type': [''],
    'description': ['I\'m a horrible scanner, a zero range weapon, and an engine that only works on Saturday'],
    'facility_level': [0, 0, 100],
    'cost': [Cost()],
    'race_requirements': [''],
    'level': [TechLevel()],
    'mass': [0, 0, sys.maxsize],
    'cargo_max': [0, 0, sys.maxsize],
    'fuel_max': [0, 0, sys.maxsize],
    'shield': [0, 0, sys.maxsize],
    'armor': [0, 0, sys.maxsize],
    'ecm': [0, 0, 100],
    'weapons': [[]], # weapon.Weapon()
    'bombs': [[]], # bomb.Bomb()
    'scanner': [Scanner()],
    'cloak': [Cloak()],
    'engines': [[]], # engine.Engine()
    'shipyard': [0, 0, sys.maxsize],
    'repair': [0, 0, sys.maxsize],
    'mines_laid': [0, 0, sys.maxsize],
    'fuel_generation': [0, 0, sys.maxsize],
    'hyperdenial': [HyperDenial()],
    'is_colonizer': [False],
    'is_starbase': [False],
    'is_trading_post': [False],
    'facility_output': [0.0, 0.0, sys.maxsize],
    'mining_rate': [0.0, 0.0, sys.maxsize],
    'mineral_depletion_factor': [0.0, 0.0, 100],
    'mat_trans_energy': [0, 0, sys.maxsize],
    'slots_general': [0, 0, sys.maxsize],
    'slots_depot': [0, 0, sys.maxsize],
    'slots_orbital': [0, 0, sys.maxsize],
}


""" Represent a tech component """
class Tech(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)

    """ Determine if the item is available for a given tech level and race """
    def is_available(self, level=None, race=None):
        if level and not self.level.is_available(level):
            return False
        if race and len(self.race_requirements) > 0:
            traits = race.list_traits()
            for requirement in self.race_requirements.split(' '):
                if requirement[0] == '-':
                    if requirement[1:] in traits:
                        return False
                elif requirement not in traits:
                    return False
        return True

    """ Calculate the scrap value """
    def scrap_value(self, race):
        if self.under_construction:
            return Cost()
        c = copy.copy(self.cost)
        complete.energy = 0
        return c * (race.scrap_rate() / 100)

    def get_display_category(self):
        if self.category in ['Beam Weapon', 'Bomb', 'Missle']:
            return 'Weapons'
        elif self.category in ['Shield', 'Armor']:
            return 'Defense'
        elif self.category in ['Cloak', 'ECM', 'Scanner']:
            return 'Electronics'
        elif self.category in ['Engine']:
            return 'Engines'
        elif self.category in ['Starbase', 'Hull', 'Mechanical']:
            return 'Hulls & Mechanicals'
        elif self.category in ['Depot', 'Orbital']:
            return 'Heavy Equipment'
        elif self.category in ['Planetary Shield', 'Planetary Scanner', 'Mineral Extracter', 'Factory', 'Power Plant']:
            return 'Planetary'        
        else:
            return 'Other'





Tech.set_defaults(Tech, __defaults)
