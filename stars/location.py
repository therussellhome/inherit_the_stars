import sys
from math import cos, pi, sin
from random import random
from . import game_engine
from . import stars_math
from .reference import Reference


""" Class defining a location """
class Location(game_engine.BaseClass):
    """ Initialize the location """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self_dict = object.__getattribute__(self, '__dict__')
        self_dict['x'] = kwargs.get('x', 0.0)
        self_dict['y'] = kwargs.get('y', 0.0)
        self_dict['z'] = kwargs.get('z', 0.0)
        if 'reference' in kwargs:
            reference = Reference(kwargs['reference'])
            if hasattr(reference, 'location'):
                self_dict['reference'] = reference
                if kwargs.get('in_system', False) or reference.location.in_system:
                    self_dict['in_system'] = True
                if 'offset' in kwargs:
                    offset = kwargs.get('offset', 0.0)
                    lat = kwargs.get('lat', random() * 180 - 90)
                    lon = kwargs.get('lon', random() * 360 - 180)
                    self_dict['x'] = round(cos(lat * pi / 180) * offset * cos(lon * pi / 180), 5)
                    self_dict['y'] = round(sin(lat * pi / 180) * offset * cos(lon * pi / 180), 5)
                    self_dict['z'] = round(sin(lon * pi / 180) * offset, 5)
        if 'random' in kwargs and kwargs['random']:
            # loop until a point is created inside a radius=1 sphere
            while True:
                x = random() * 2 - 1
                y = random() * 2 - 1
                z = random() * 2 - 1
                if stars_math.distance(x, y, z, 0, 0, 0) <= 1.0:
                    self_dict['x'] = x * kwargs.get('scale_x', 1.0)
                    self_dict['y'] = y * kwargs.get('scale_y', 1.0)
                    self_dict['z'] = z * kwargs.get('scale_z', 1.0)
                    break
    
    #def polar_offset(dis, lat, lon):
    #    x = round(cos(lat*pi/180)*dis*cos(lon*pi/180), 5)
    #    y = round(sin(lat*pi/180)*dis*cos(lon*pi/180), 5)
    #    z = round(sin(lon*pi/180)*dis, 5)
    #    return Location(x = self.x + x, y = self.y + y, z = self.z + z)

    #def intercept(self, target, max_distance, standoff=0.0, target_prev=None):
    #    distance = (self - target) - standoff
    #    f = max_distance / distance
    #    x = self.x - (self.x - target.x) * f
    #    y = self.y - (self.y - target.y) * f
    #    z = self.z - (self.z - target.z) * f
    #    return Location(x=x, y=y, z=z)

    """ returns the location to move to """
    def move(self, target, max_distance, away=False, standoff=0.0, target_prev=None):
        #target = self.intercept(target, max_distance, standoff, target_prev)
        distance = self - target
        move_distance = max_distance
        if distance - max_distance < standoff:
            if distance < standoff:
                away = True
                if max_distance > standoff:
                    move_distance = standoff - distance
            else:
                move_distance = distance - standoff
        if distance == 0:
            return self
        if not away:
            f = min(1, move_distance / distance)
        else:
            f = -1 * move_distance / distance
        x = self.x - (self.x - target.x) * f
        y = self.y - (self.y - target.y) * f
        z = self.z - (self.z - target.z) * f
        return Location(x=x, y=y, z=z)
    
    """ Distance between 2 points """
    def __sub__(self, other):
        return stars_math.distance(self.x, self.y, self.z, other.x, other.y, other.z)
    
    """ Equality check """
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z and getattr(self, 'reference', None) == getattr(other, 'reference', None)

    """ If a reference then get the attribute from the referenced class """
    def __getattribute__(self, name):
        self_dict = object.__getattribute__(self, '__dict__')
        if 'reference' in self_dict and name == 'x':
            return self_dict['reference'].location.x + self_dict['x']
        elif 'reference' in self_dict and name == 'y':
            return self_dict['reference'].location.y + self_dict['y']
        elif 'reference' in self_dict and name == 'z':
            return self_dict['reference'].location.z + self_dict['z']
        elif name == 'in_system':
            return self_dict.get('in_system', False)
        else:
            return object.__getattribute__(self, name)

    """ Set the attribute locally """
    def __setattr__(self, name, value):
        self_dict = object.__getattribute__(self, '__dict__')
        self_dict[name] = value
