import sys
from .tech import Tech
from .engine import Engine
from .scanner import Scanner
from .weapon import Weapon


""" Default values (default, min, max)  """
__defaults = {
    'mass': [0, 0, sys.maxsize],
    'cargo_max': [0, 0, sys.maxsize],
    'fuel_max': [0, 0, sys.maxsize],
    'shield': [0, 0, sys.maxsize],
    'armor': [0, 0, sys.maxsize],
    'ecm': [0, 0, 100],
    'weapons': [[]], # weapon.Weapon()
    'scanners': [[]], # scanner.Scanner()
    'cloak': [0, 0, 100],
    'engines': [[]], # engine.Engine()
    'initiative': [0, 0, sys.maxsize],
    'repair': [0, 0, sys.maxsize],
    'fuel_generation': [0, 0, sys.maxsize],
    'special_type': [''],
    'colonizer': [False],
}


""" Represent 'component' """
class Component(Tech):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Component.set_defaults(Component, __defaults)
