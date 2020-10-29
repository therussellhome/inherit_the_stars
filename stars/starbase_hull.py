import sys
from . import game_engine
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'general_slots': [],
    'orbital_slots': [],
    'max_pop':[],
}

class StarbaseHull(Component):
    pass

StarbaseHull.set_defaults(StarbaseHull, __defaults)
