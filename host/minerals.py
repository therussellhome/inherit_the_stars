import sys
from . import game_engine

""" Default values (default, min, max)  """
__defaults = {
    'titanium': [0, 0, sys.maxsize],
    'lithium': [0, 0, sys.maxsize],
    'silicon': [0, 0, sys.maxsize]
}

""" Represent 'minerals' """
class Minerals(game_engine.Defaults):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Minerals, defaults=__defaults)
