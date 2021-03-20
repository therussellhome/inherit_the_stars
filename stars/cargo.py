import sys
from .minerals import Minerals


""" Default values (default, min, max)  """
__defaults = {
    'people': (0.0, 0.0, sys.maxsize),
    'cargo_max': (0, -1, sys.maxsize),
}


""" Represent 'cargo' that can be held """
class Cargo(Minerals):
    def __getattribute__(self, name):
        if name == 'cargo_max' and super().__getattribute__(name) == -1:
            return sys.maxsize
        else:
            return super().__getattribute__(name)
    
    """ Provide an addition operator """
    def __add__(self, other):
        m = super().__add__(other)
        c = Cargo(**m.__dict__)
        c.people = self.people + getattr(other, 'people', 0)
        c.cargo_max = self.cargo_max + getattr(other, 'cargo_max', 0)
        return c

    def _sum(self):
        return (self.titanium + self.lithium + self.silicon + self.people)

    def percent_full(self):
        return self._sum() / self.cargo_max

Cargo.set_defaults(Cargo, __defaults)
