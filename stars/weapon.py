import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'power': [0, 0, sys.maxsize],
    'shield_multiplier': [0, 0, 200],
    'armor_multiplier': [0, 0, 200],
    'is_beam': [True],
    'is_multishot': [False],
    'range': [0, 0, sys.maxsize],
    'accuracy': [100, 0, 100]
}

""" Represent 'a weapon' """
class Weapon(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Weapon.set_defaults(Weapon, __defaults)
