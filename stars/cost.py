import sys
from .minerals import Minerals


""" Default values (default, min, max)  """
__defaults = {
    'energy': [0, 0, sys.maxsize]
}


""" Represent 'cost' """
class Cost(Minerals):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def __eq__(self, other):
        if super().__eq__(other) and self.energy == other.energy:
            return True
        return False


    def __add__(self, other):
        m = super().__add__(other)
        c = Cost(**m.__dict__)
        c.energy = self.energy + other.energy
        return c


    def __sub__(self, other):
        m = super().__sub__(other)
        c = Cost(**m.__dict__)
        c.energy = self.energy - other.energy
        return c


Cost.set_defaults(Cost, __defaults)
