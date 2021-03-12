import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'energy': (0, 0, sys.maxsize),
    'minerals': (0, 0, sys.maxsize),
    'tech_levels': (0, 0, sys.maxsize),
    'planets': (0, 0, sys.maxsize),
    'ships_unarmed': (0, 0, sys.maxsize),
    'ships_escort': (0, 0, sys.maxsize),
    'ships_of_the_wall': (0, 0, sys.maxsize),
    'facilities': (0, 0, sys.maxsize),
    'starbases': (0, 0, sys.maxsize),
    'rank': (1, 1, sys.maxsize),
}


""" Represent 'score' """
class Score(Defaults):
    pass


Score.set_defaults(Score, __defaults)
