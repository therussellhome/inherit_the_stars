import sys
from .minerals import Minerals


""" Default values (default, min, max)  """
__defaults = {
    'people': [0.0, 0.0, sys.maxsize],
    'cargo_max': [0, -1, sys.maxsize]
}


""" Represent 'cargo' that can be held """
""" A cargo_max of -1 is used to indicate no maximum """
class Cargo(Minerals):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __getattribute__(self, name):
        if name == 'cargo_max' and super().__getattribute__(name) == -1:
            return sys.maxsize
        else:
            return super().__getattribute__(name)
    
    def __add__(self, other):
        m = super().__add__(other)
        c = Cargo(**m.__dict__)
        c.people = self.people + other.people
        c.cargo_max = self.cargo_max + other.cargo_max
        return c

    def _sum(self):
        return (self.titanium + self.lithium + self.silicon + self.people)

    def percent_full(self):
        return self._sum() / self.cargo_max

Cargo.set_defaults(Cargo, __defaults)
