import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'titanium': (0.0, 0.0, sys.maxsize),
    'lithium': (0.0, 0.0, sys.maxsize),
    'silicon': (0.0, 0.0, sys.maxsize),
}


""" List of mineral types """
MINERAL_TYPES = ['titanium', 'lithium', 'silicon']


""" Represent 'minerals' """
class Minerals(Defaults):
    """ Test if the minerals are zero """
    def is_zero(self):
        return (self.titanium == 0 and self.lithium == 0 and self.silicon == 0)

    """ Addition operator """
    def __add__(self, other):
        m = Minerals()
        m.titanium = self.titanium + other.titanium
        m.lithium = self.lithium + other.lithium
        m.silicon = self.silicon + other.silicon
        return m

    """ Subtracton operator """
    def __sub__(self, other):
        m = Minerals()
        m.titanium = self.titanium - other.titanium
        m.lithium = self.lithium - other.lithium
        m.silicon = self.silicon - other.silicon
        return m

    """ Mutiply operator """
    def __mul__(self, other):
        m = Minerals()
        m.titanium = self.titanium * other
        m.lithium = self.lithium * other
        m.silicon = self.silicon * other
        return m


Minerals.set_defaults(Minerals, __defaults)
