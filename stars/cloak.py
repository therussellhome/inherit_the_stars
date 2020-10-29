import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'percent': [0, 0, 100]
}


""" Represent 'cloak' """
class Cloak(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __add__(self, other):
        v = 100 - self.percent
        v = 100 - (v - v * other.percent / 100)
        return Cloak(percent=v)


Cloak.set_defaults(Cloak, __defaults)
