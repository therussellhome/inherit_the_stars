import sys
from . import game_engine
from .defaults import Defaults
from .tech import Tech


""" Default values (default, min, max)  """
__defaults = {
    'general_slots': [0, 0, sys.maxsize],
    'depot_slots': [0, 0, sys.maxsize],
}

class ShipHull(Tech):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

ShipHull.set_defaults(ShipHull, __defaults)
