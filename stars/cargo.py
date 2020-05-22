import sys
from .minerals import Minerals


""" Default values (default, min, max)  """
__defaults = {
    'people': [0, 0, sys.maxsize],
    'cargo_max': [0, 0, sys.maxsize]
}


""" Represent 'cargo' that can be held """
""" A cargo_max of -1 is used to indicate no maximum """
class Cargo(Minerals):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Cargo.set_defaults(Cargo, __defaults)
