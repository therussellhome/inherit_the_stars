import sys
from .tech import Tech
from .cargo import Cargo
from .cloak import Cloak
from .engine import Engine
from .scanner import Scanner
from .weapon import Weapon


""" Default values (default, min, max)  """
__defaults = {
    'mass': [0, 0, sys.maxsize],
    'cargo': [Cargo()],
    'fuel_max': [0, 0, sys.maxsize],
    'shield': [0, 0, sys.maxsize],
    'armor': [0, 0, sys.maxsize],
    'weapon': [Weapon()],
    'ecm': [0, 0, 100],
    'targeting': [0, 0, 100],
    'engine': [Engine()],
    'scanner': [Scanner()],
    'cloak': [Cloak()],
    'initiative': [0, 0, sys.maxsize],
    'repair': [0, 0, sys.maxsize],
    'fuel_generation': [0, 0, sys.maxsize],
    'special_type': ['']
    'colonizer': [False]
}


""" Represent 'minerals' """
class Component(Tech):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Component.set_defaults(Component, __defaults)
