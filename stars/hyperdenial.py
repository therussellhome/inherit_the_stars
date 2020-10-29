import sys
from . import stars_math
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'range': [0.0, 0.0, sys.maxsize],
}


""" Represent 'hyperdenial' """
class HyperDenial(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __add__(self, other):
        h = HyperDenial()
        h.range = stars_math.volume_add(self.range, other.range)
        return h

HyperDenial.set_defaults(HyperDenial, __defaults)
