import sys
from .minerals import Minerals


""" Default values (default, min, max)  """
__defaults = {
    'people': (0.0, 0.0, sys.maxsize),
}


""" List of mineral types """
CARGO_TYPES = ['titanium', 'lithium', 'silicon', 'people']


""" Represent 'cargo' that can be held """
class Cargo(Minerals):
    """ Provide an addition operator """
    def __add__(self, other):
        m = super().__add__(other)
        c = Cargo(**m.__dict__)
        c.people = self.people + getattr(other, 'people', 0)
        return c

    """ Total the contents """
    def sum(self):
        return (self.titanium + self.lithium + self.silicon + self.people)

Cargo.set_defaults(Cargo, __defaults)
