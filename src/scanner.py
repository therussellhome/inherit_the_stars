import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'anti_cloak': [0, 0, sys.maxsize],
    'penetrating': [0, 0, sys.maxsize],
    'range_for_100kt': [50, 0, sys.maxsize]
}


""" Represent 'scanner' """
class Scanner(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Scanner.set_defaults(Scanner, __defaults)
