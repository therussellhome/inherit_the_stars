import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'x': [0.0, -sys.maxsize, sys.maxsize],
    'y': [0.0, -sys.maxsize, sys.maxsize],
    'z': [0.0, -sys.maxsize, sys.maxsize],
}

""" Class defining a location """
class Location(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    TM_2_LY = 0.000105702977392

class LocationReference:
    """ Initialize defaults """
    def __init__(self, **kwargs):
        self.reference = kwargs['reference']

    """ Get the attribute from the real class """
    def __getattribute__(self, name):
        if name == 'x':
            return self.reference.location.x
        elif name == 'y':
            return self.reference.location.y
        elif name == 'z':
            return self.reference.location.z
        else:
            return object.__getattribute__(self, name)
