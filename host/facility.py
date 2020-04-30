import sys
import game_engine
from tech import Tech


""" Default values (default, min, max)  """
__defaults = {
    'output_per_facility': [0.0, 0.0, sys.maxsize],
    'effort_per_facility': [1000, 0, sys.maxsize]
}

""" Represent 'minerals' """
class Facility(Tech):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Facility, defaults=__defaults)
