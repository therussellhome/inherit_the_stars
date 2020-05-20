import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'energy': [0, 0, sys.maxsize],
    'weapons': [0, 0, sys.maxsize],
    'propulsion': [0, 0, sys.maxsize],
    'construction': [0, 0, sys.maxsize],
    'electronics': [0, 0, sys.maxsize],
    'biotechnology': [0, 0, sys.maxsize]
}

""" Represent 'cost' """
class TechLevel(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


TechLevel.set_defaults(TechLevel, __defaults)
