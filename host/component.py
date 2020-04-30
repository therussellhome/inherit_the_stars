import sys
import game_engine
from tech import Tech
from cargo import Cargo
from engine import Engine
from weapon import Weapon


""" Default values (default, min, max)  """
__defaults = {
    'mass': [0, 0, sys.maxsize],
    'cargo': [Cargo('cargo_max'=0)],
    'fuel': [0, 0, sys.maxsize],
    'armor': [0, 0, sys.maxsize],
    'shield': [0, 0, sys.maxsize],
    'weapon': [Weapon()],
    'engine': [Engine()],
    'initiative': [0, 0, sys.maxsize],
    'repair': [0, 0, sys.maxsize],
    'fuel_generation': [0, 0, sys.maxsize],
    'special_type': ['']
    'colonizer': [False]
}

""" Represent 'minerals' """
class Component(Tech):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Component, defaults=__defaults)
