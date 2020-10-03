import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'titanium': [0, 0, sys.maxsize],
    'lithium': [0, 0, sys.maxsize],
    'silicon': [0, 0, sys.maxsize]
}


""" Represent 'minerals' """
class Minerals(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def __eq__(self, other):
        if self.titanium == other.titanium and self.lithium == other.lithium and self.silicon == other.silicon:
            return True
        return False


    def __add__(self, other):
        m = Minerals()
        m.titanium = self.titanium + other.titanium
        m.lithium = self.lithium + other.lithium
        m.silicon = self.silicon + other.silicon
        return m


    def __sub__(self, other):
        m = Minerals()
        m.titanium = self.titanium - other.titanium
        m.lithium = self.lithium - other.lithium
        m.silicon = self.silicon - other.silicon
        return m


Minerals.set_defaults(Minerals, __defaults)
