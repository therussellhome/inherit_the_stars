import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'energy': [0, 0, sys.maxsize],
    'minerals': [0, 0, sys.maxsize],
    'tech_levels': [0, 0, sys.maxsize],
    'planets': [0, 0, sys.maxsize],
    'ships_unarmed': [0, 0, sys.maxsize],
    'ships_escort': [0, 0, sys.maxsize],
    'ships_of_the_wall': [0, 0, sys.maxsize],
    'facilities': [0, 0, sys.maxsize],
    'starbases': [0, 0, sys.maxsize],
    'rank': [16, 1, 16],
}


""" Represent 'score' """
class Score(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Score.set_defaults(Score, __defaults)
