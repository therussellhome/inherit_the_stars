import sys
from . import stars_math
from .defaults import Defaults


""" Reset the hyperdenials """
def reset(reset_all=False):
    pass #TODO

""" Add a hyperdenial zone """
def add(location, radius, persistant=True):
    pass #TODO

""" Calculate the number of denials passed through """
def transit(start, stop):
    return 0 #TODO


""" Default values (default, min, max)  """
__defaults = {
    'radius': (0.0, 0.0, sys.maxsize),
}


""" Represent 'hyperdenial' """
class HyperDenial(Defaults):
    """ Addition operator """
    def __add__(self, other):
        h = HyperDenial()
        h.radius = stars_math.volume_add(self.radius, other.radius)
        return h

    """ Activate the hyperdenial """
    def activate(self, location):
        if self.radius > 0:
            add(location, self.radius, False)

HyperDenial.set_defaults(HyperDenial, __defaults)
