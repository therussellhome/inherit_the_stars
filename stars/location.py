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

    """ Distance between 2 points """
    def __sub__(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5
    
Location.set_defaults(Location, __defaults)

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

    """ Distance between 2 points """
    def __sub__(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5
    
