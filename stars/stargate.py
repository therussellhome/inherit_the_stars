import sys
from . import stars_math
from random import random
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
    
    def overgate(self, mass, distance, experience=1, survival_test=False):
        amt = max(mass + distance - self.strength, 0)
        #print(amt)
        per = amt / self.strength
        min_dam = (per + amt/1000.0)**1.3 * 512 #TODO IT.
        #print(min_dam)
        if survival_test:
            return min_dam
        luck = random() * 5/experience
        return min_dam * (1 + luck)


Stargate.set_defaults(Stargate, __defaults)
