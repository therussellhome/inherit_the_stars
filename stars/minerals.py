import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'titanium': [0, 0, sys.maxsize],
    'lithium': [0, 0, sys.maxsize],
    'silicon': [0, 0, sys.maxsize]
}


""" Represent 'minerals' """
class Minerals(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Minerals.set_defaults(Minerals, __defaults)
