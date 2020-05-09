import sys
from . import game_engine
from . import minerals

""" Default values (default, min, max)  """
__defaults = {
    'people': [0, 0, sys.maxsize],
    'cargo_max': [0, 0, sys.maxsize]
}

""" Represent 'cargo' that can be held """
""" A cargo_max of -1 is used to indicate no maximum """
class Cargo(minerals.Minerals):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Cargo, defaults=__defaults)
