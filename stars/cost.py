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


Cost.set_defaults(Cost, __defaults)
