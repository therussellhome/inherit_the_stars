import sys
from .defaults import Defaults
from .cost import Cost
from .tech_level import TechLevel
from .scanner import Scanner


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
    'scanner': [Scanner], # scanner.Scanner()
    'cloak': [0, 0, 100],
    'engines': [[]], # engine.Engine()
    'shipyard': [0, 0, sys.maxsize],
    'repair': [0, 0, sys.maxsize],
    'fuel_generation': [0, 0, sys.maxsize],
    'hyperdenial': [0, 0, sys.maxsize],
    'special_type': [''],
    'colonizer': [False],
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
        if level.is_available(player.tech_level):
            # TODO check race requirements
            return True
        return False

    """ Stack the scanners """
    def stack_scanners(self):
        stack = None
        for scanner in self.scanners:
            if not stack:
                stack = scanner
            else:
                stack = stack.stack(scanner)
        return stack

Tech.set_defaults(Tech, __defaults)
