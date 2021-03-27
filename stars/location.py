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
    'is_system': False,
    'reference': Reference(''),
    'offset': 0.0,
    'orbit_lon': 0.0,
    'orbit_speed': 0.0,
}


""" Class defining a location """
class Location(Defaults):
    """ Initialize the location """
    def __init__(self, **kwargs):
        if 'new_random' in kwargs:
            # loop until a point is created inside a radius=1 sphere
            p = (1.0, 1.0, 1.0)
            while stars_math.distance(*p, 0, 0, 0) > 1.0:
                p = (random() * 2 - 1, random() * 2 - 1, random() * 2 - 1)
            kwargs['x'] = p[0] * kwargs['new_random'][0]
            kwargs['y'] = p[1] * kwargs['new_random'][1]
            kwargs['z'] = p[2] * kwargs['new_random'][2]
            del kwargs['new_random']
        elif 'new_orbit' in kwargs:
            kwargs['orbit_speed'] = kwargs['new_orbit']
            kwargs['orbit_lon'] = random() * 360 - 180
            del kwargs['new_orbit']
        if 'reference' in kwargs:
            kwargs['reference'] = Reference(kwargs['reference'])
        super().__init__(**kwargs)
    
    """ Orbit """
    def orbit():
        if self.orbit_speed > 0:
            self.orbit_lon += self.orbit_speed
            if self.orbit_lon > 180:
                self.orbit_lon - 180
            # Force recalc of xyz
            self.__dict__['__cache__'] = {}

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
        self_xyz = self.xyz
        target_xyz = target.xyz
        return Location(
            x = self_xyz[0] - (self_xzy[0] - target_xyz[0]) * f,
            y = self_xyz[1] - (self_xyz[1] - target_xyz[1]) * f,
            z = self_xyz[2] - (self_xyz[2] - target_xyz[2]) * f)

    """ Distance between 2 points """
    def __sub__(self, other):
        return stars_math.distance(self.x, self.y, self.z, other.x, other.y, other.z)
    
    """ If a reference then get the attribute from the referenced class """
    def __getattribute__(self, name):
        self_dict = object.__getattribute__(self, '__dict__')
        cache = self_dict.get('__cache__', None)
        # No cache so passthrough
        if not cache:
            return object.__getattribute__(self, name)
        # Check if reference has changed
        elif self_dict['reference']:
            # convert/reconert to absolute
            ref_xyz = self_dict['reference'].location.xyz
            if 'ref_xyz' not in cache or cache['ref_xyz'] != ref_xyz:
                cache['ref_xyz'] = ref_xyz
                cache['ref_root'] = reference.location.reference_root
                # location does not have a fixed xyz offset
                if self_dict['offset'] == 0.0:
                    cache['xyz'] = (ref_xyz[0] + self_dict['x'], ref_xyz[1] + self_dict['y'], ref_xyz[2] + self_dict['z'])
                else:
                    if self_dict['orbit_speed'] > 0:
                        lat = 0
                        lon = self_dict['orbit_lon']
                    else:
                        lat = random() * 180 - 90
                        lon = random() * 360 - 180
                    cache['xyz'] = (
                        ref_xyz[0] + round(cos(lat * pi / 180) * self_dict['offset'] * cos(lon * pi / 180), 5),
                        ref_xyz[1] + round(sin(lat * pi / 180) * self_dict['offset'] * cos(lon * pi / 180), 5),
                        ref_xyz[2] + round(sin(lon * pi / 180) * self_dict['offset'], 5))
        # Created cached version
        elif 'xyz' not in cache:
            cache['ref_root'] = self
            cache['xyz'] = (self_dict['x'], self_dict['y'], self_dict['z'])
        if name == 'xyz':
            return cache['xyz']
        if name == 'x':
            return cache['xyz'][0]
        if name == 'y':
            return cache['xyz'][1]
        if name == 'z':
            return cache['xyz'][2]
        if name == 'reference_root':
            return cache['ref_root']
        if name == 'in_system':
            return cache['ref_root'].is_system
        return object.__getattribute__(self, name)

    """ Use the absolute position as the hash """
    def __hash__(self):
        return hash(self.xyz)


Location.set_defaults(Location, __defaults)
