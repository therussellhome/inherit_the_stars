import sys
from math import cos, pi, sin
from random import random
from . import stars_math
from .defaults import Defaults
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'x': 0.0,
    'y': 0.0,
    'z': 0.0,
    'in_system': False,
    'reference': Reference(''),
    'offset': 0.0,
}


""" Class defining a location """
class Location(Defaults):
    """ Initialize the location """
    def __init__(self, **kwargs):
        if 'random_in' in kwargs:
            # loop until a point is created inside a radius=1 sphere
            p = (1.0, 1.0, 1.0)
            while stars_math.distance(*p, 0, 0, 0) > 1.0:
                p = (random() * 2 - 1, random() * 2 - 1, random() * 2 - 1)
            kwargs['x'] = p[0] * kwargs['random_in'][0]
            kwargs['y'] = p[1] * kwargs['random_in'][1]
            kwargs['z'] = p[2] * kwargs['random_in'][2]
            del kwargs['random_in']
        super().__init__(**kwargs)
        if 'reference' in kwargs:
            self.reference = Reference(kwargs['reference'])
    
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
    
    """ If a reference then get the attribute from the referenced class """
    def __getattribute__(self, name):
        self_dict = object.__getattribute__(self, '__dict__')
        if '__cache__' not in self_dict:
            return object.__getattribute__(self, name)
        if self_dict['__cache__'] == {}:
            # location is relative but has not been converted to absolute
            if self_dict['reference']:
                # location does not have a fixed offset
                if self_dict['offset'] != 0.0:
                    lat = random() * 180 - 90
                    lon = random() * 360 - 180
                    self_dict['x'] = round(cos(lat * pi / 180) * self_dict['offset'] * cos(lon * pi / 180), 5)
                    self_dict['y'] = round(sin(lat * pi / 180) * self_dict['offset'] * cos(lon * pi / 180), 5)
                    self_dict['z'] = round(sin(lon * pi / 180) * self_dict['offset'], 5)
                self_dict['__cache__'] = (
                        self_dict['reference'].location.x + self_dict['x'],
                        self_dict['reference'].location.y + self_dict['y'],
                        self_dict['reference'].location.z + self_dict['z'])
            else:
                self_dict['__cache__'] = (self_dict['x'], self_dict['y'], self_dict['z'])
        # if relative then get the in_system flag from the referenced location
        if name == 'in_system' and self_dict['reference']:
            return self_dict['reference'].locaton.in_system
        elif name == 'x':
            return self_dict['__cache__'][0]
        elif name == 'y':
            return self_dict['__cache__'][1]
        elif name == 'z':
            return self_dict['__cache__'][2]
        else:
            return object.__getattribute__(self, name)


Location.set_defaults(Location, __defaults)
