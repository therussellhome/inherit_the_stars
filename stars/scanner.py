import sys
from . import stars_math
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'anti_cloak': (0.0, 0.0, sys.maxsize),
    'penetrating': (0.0, 0.0, sys.maxsize),
    'normal': (0.0, 0.0, sys.maxsize),
}


""" Represent 'scanner' """
class Scanner(Defaults):
    """ Addition operator """
    def __add__(self, other):
        s = Scanner()
        s.anti_cloak = stars_math.volume_add(self.anti_cloak, other.anti_cloak)
        s.penetrating = stars_math.volume_add(self.penetrating, other.penetrating)
        s.normal = stars_math.volume_add(self.normal, other.normal) 
        return s


Scanner.set_defaults(Scanner, __defaults)
