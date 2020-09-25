import sys
from .cloak import Cloak
from .cost import Cost
from .defaults import Defaults
from .hyperdenial import HyperDenial
from .scanner import Scanner
from .tech_level import TechLevel


""" Default values (default, min, max)  """
__defaults = {
    'name': [''],
    'category': [''],
    'slot_type': [''],
    'description': ['I\'m a horrible scanner, a zero range weapon, and an engine that only works on Saturday'],
    'upgrade_path': [''],
    'upgrade_level': [0, 0, 100],
    'race_requirements': [''],
    'cost': [Cost()],
    'cost_build_complete': [Cost()],
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
    'fuel_generation': [0, 0, sys.maxsize],
    'hyperdenial': [HyperDenial()],
    'is_colonizer': [False],
    'is_trading_post': [False],
    'facility_output': [0.0, 0.0, sys.maxsize],
    'mineral_depletion_rate': [0, 0, 100],
    'mat_trans_energy': [0, 0, sys.maxsize],
    'slots_general': [0, 0, sys.maxsize],
    'slots_depot': [0, 0, sys.maxsize],
    'slots_orbital': [0, 0, sys.maxsize],
}


""" Represent 'minerals' """
class Tech(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'Tech the GM made up himself ' + str(id(self))

    """ Determine if the item is available for a player's tech level """
    def is_available(self, player):
        if self.level.is_available(player.tech_level):
            # TODO check race requirements
            return True
        return False

Tech.set_defaults(Tech, __defaults)
