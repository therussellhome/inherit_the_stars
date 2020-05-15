import sys
from . import game_engine
from .minerals import Minerals

""" Default values (default, min, max)  """
__defaults = {
    'production_capacity': [0, 0, sys.maxsize],
    'energy': [0, 0, sys.maxsize],
    'effort': [0, 0, sys.maxsize]
}

""" Represent 'cost' """
class Cost(Minerals):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Cost, defaults=__defaults)
