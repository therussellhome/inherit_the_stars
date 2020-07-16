import sys
from random import random
from . import game_engine
from . import stars_math
from .reference import Reference


""" Class defining a location """
class Location(game_engine.BaseClass):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        self.x = kwargs.get('x', 0.0)
        self.y = kwargs.get('y', 0.0)
        self.z = kwargs.get('z', 0.0)
    """ returns the location to move to """
    def move(self, target, max_distance, away=False):
        if not away:
            f = min(1, max_distance / (self-target))
        else:
            f = -max_distance / (self-target)
        x = self.x + (self.x-target.x)*f
        y = self.y + (self.y-target.y)*f
        z = self.z + (self.z-target.z)*f
        return Loction(x, y, z)
    """ Distance between 2 points """
    def __sub__(self, other):
        return stars_math.distance(self.x, self.y, self.z, other.x, other.y, other.z)


""" 
Location that is actually a reference to something else's location
Reference must have a location attribute
"""
class LocationReference(Location):
    """ Initialize defaults """
    def __init__(self, *args, **kwargs):
        if 'reference' in kwargs:
            self.reference = kwargs['reference']
        else:
            self.reference = Reference(args[0])

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


def rand_location(radius_x=1.0, radius_y=1.0, radius_z=1.0):
    # loop until a point is created inside a r=1 sphere
    while True:
        x = random() * 2 - 1
        y = random() * 2 - 1
        z = random() * 2 - 1
        if stars_math.distance(x, y, z, 0, 0, 0) <= 1.0:
            return Location(x=x * radius_x, y=y * radius_y, z=z * radius_z)
