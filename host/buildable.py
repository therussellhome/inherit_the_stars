import sys
from . import game_engine
from .cost import Cost

""" Default values (default, min, max)  """
__defaults = {
    'cost': [Cost()],
    'cost_complete': [Cost()],
    'is_end_item': [False]
}

""" Represent 'cost' """
class Buildable(game_engine.Defaults):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Buildable, defaults=__defaults)
