import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'percent': [0, 0, 100],
    'kT': [0, 0, sys.maxsize]
}


""" Represent 'cloaking' """
class Scanner(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


Scanner.set_defaults(Scanner, __defaults)
