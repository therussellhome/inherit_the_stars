import sys
from . import stars_math
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'strength': (0.0, 0.0, sys.maxsize),
}


""" Represent 'stargate' """
class Stargate(Defaults):
    """ Addition operator """
    def __add__(self, other):
        s = Stargate()
        s.strength = max(self.strength, other.strength)
        return s


Stargate.set_defaults(Stargate, __defaults)
