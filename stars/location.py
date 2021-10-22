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
    'orbit_lon': 0.0, #degrees
    'orbit_speed': 0.0, # degrees
}


""" Class defining a location """
class Location(Defaults):
    """ Initialize the location """
    def __init__(self, *args, **kwargs):
        if len(args) == 3:
            kwargs['x'] = args[0]
            kwargs['y'] = args[1]
            kwargs['z'] = args[2]
        elif 'new_random' in kwargs:
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
    def orbit(self):
        if self.orbit_speed > 0:
            self.orbit_lon += self.orbit_speed
            if self.orbit_lon > 360:
                self.orbit_lon - 360
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
            x = self_xyz[0] - (self_xyz[0] - target_xyz[0]) * f,
            y = self_xyz[1] - (self_xyz[1] - target_xyz[1]) * f,
            z = self_xyz[2] - (self_xyz[2] - target_xyz[2]) * f)

    """ Comparison allowing for close enough """
    def __eq__(self, other):
        if isinstance(other, Location):
            if self - other < stars_math.TERAMETER_2_LIGHTYEAR / 1000:
                return True
        return False

    """ Returns the cardinal direction of itself reletive to another location object """
    def get_cardinal_direction(self, other):
        distance = self - other
        if distance == 0:
            return
        self_xyz = self.xyz
        other_xyz = other.xyz
        x = self_xyz[0] - other_xyz[0]
        y = self_xyz[1] - other_xyz[1]
        z = self_xyz[2] - other_xyz[2]
        zcardinal = ['N', 'S']
        xcardinal = ['E', 'W']
        ycardinal = ['U', 'D']
        cardinal = str(distance) + ' '
        if abs(z) / distance > 0.25:
            if z < 0:
                cardinal += zcardinal[1]
            else:
                cardinal += zcardinal[0]
        if abs(x) / distance > 0.25:
            if x < 0:
                cardinal += xcardinal[1]
            else:
                cardinal += xcardinal[0]
        if abs(y) / distance > 0.25:
            if y < 0:
                cardinal += ycardinal[1]
            else:
                cardinal += ycardinal[0]
        return cardinal

    """ Distance between 2 points """
    def __sub__(self, other):
        self_xyz = self.xyz
        other_xyz = other.xyz
        return stars_math.distance(self_xyz[0], self_xyz[1], self_xyz[2], other_xyz[0], other_xyz[1], other_xyz[2])
    
    """ If a reference then get the attribute from the referenced class """
    def __getattribute__(self, name):
        self_dict = object.__getattribute__(self, '__dict__')
        # No cache so passthrough
        if '__cache__' not in self_dict:
            return object.__getattribute__(self, name)
        cache = self_dict['__cache__']
        # Check if reference has changed
        if self_dict['reference']:
            # convert/reconert to absolute
            ref_xyz = self_dict['reference'].location.xyz
            if 'ref_xyz' not in cache or cache['ref_xyz'] != ref_xyz:
                cache['ref_xyz'] = ref_xyz
                cache['root_location'] = self_dict['reference'].location.root_location
                root_ref = self_dict['reference'].location.root_reference
                if root_ref:
                    cache['root_reference'] = root_ref
                else:
                    cache['root_reference'] = self_dict['reference']
                # location does not have a fixed xyz offset
                if self_dict['offset'] == 0.0:
                    cache['xyz'] = (ref_xyz[0] + self_dict['x'], ref_xyz[1] + self_dict['y'], ref_xyz[2] + self_dict['z'])
                else:
                    if self_dict['orbit_speed'] > 0.0:
                        lat = 0
                        lon = self_dict['orbit_lon']
                    else:
                        lat = random() * 180 - 90
                        lon = random() * 360 - 180
                    cache['xyz'] = (
                        ref_xyz[0] + self_dict['offset'] * round(cos(lat * pi / 180) * cos(lon * pi / 180), 10),
                        ref_xyz[1] + self_dict['offset'] * round(cos(lat * pi / 180) * sin(lon * pi / 180), 10),
                        ref_xyz[2] + self_dict['offset'] * round(sin(lat * pi / 180), 10))
        # Created cached version
        elif 'xyz' not in cache:
            cache['root_location'] = self
            cache['root_reference'] = None
            cache['xyz'] = (self_dict['x'], self_dict['y'], self_dict['z'])
        if name == 'xyz':
            return cache['xyz']
        if name == 'x':
            return cache['xyz'][0]
        if name == 'y':
            return cache['xyz'][1]
        if name == 'z':
            return cache['xyz'][2]
        if name == 'root_location':
            return cache['root_location']
        if name == 'root_reference':
            return cache['root_reference']
        if name == 'in_system':
            return cache['root_location'].is_system
        return object.__getattribute__(self, name)

    """ Use the absolute position as the hash """
    def __hash__(self):
        return hash(self.xyz)


Location.set_defaults(Location, __defaults)
