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

""" Temporary values (default, min, max)  """
__tmp_defaults = {
    'xyz': None,
    'ref_xyz': None,
    'relative_xyz': None,
    'root_location': None,
    'root_reference': None,
}


""" Class defining a location """
class Location(Defaults):
    """ Initialize the location """
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], Location):
            kwargs['x'] = args[0].x
            kwargs['y'] = args[0].y
            kwargs['z'] = args[0].z
        elif len(args) == 3:
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
            if self.orbit_lon > 180:
                self.orbit_lon - 180
            # Force recalc of xyz
            self.__dict__['xyz'] = None

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
        return Location(
            x = self.xyz[0] - (self.xyz[0] - target.xyz[0]) * f,
            y = self.xyz[1] - (self.xyz[1] - target.xyz[1]) * f,
            z = self.xyz[2] - (self.xyz[2] - target.xyz[2]) * f)

    """ Comparison allowing for close enough """
    def __eq__(self, other):
        if isinstance(other, Location):
            if self - other < stars_math.TERAMETER_2_LIGHTYEAR / 1000:
                return True
        return False

    """ Distance between 2 points """
    def __sub__(self, other):
        return stars_math.distance(self.xyz[0], self.xyz[1], self.xyz[2], other.xyz[0], other.xyz[1], other.xyz[2])
    
    """ Provide calculated values """
    def __getattribute__(self, name):
        self_dict = object.__getattribute__(self, '__dict__')
        # Safety check if inital defaults have not been applied
        if '__init_complete__' not in self_dict:
            return super().__getattribute__(name)
        # Check if reference has changed
        if self_dict['reference']:
            # convert/reconert to absolute
            ref_xyz = self_dict['reference'].location.xyz
            if self_dict['xyz'] is None or self_dict['ref_xyz'] is None or self_dict['ref_xyz'] != ref_xyz:
                self_dict['ref_xyz'] = ref_xyz
                self_dict['root_location'] = self_dict['reference'].location.root_location
                self_dict['root_reference'] = self_dict['reference'].location.root_reference
                if not self_dict['root_reference']:
                    self_dict['root_reference'] = self_dict['reference']
                # location does not have a fixed xyz offset
                if self_dict['offset'] == 0.0:
                    self_dict['relative_xyz'] = (self_dict['x'], self_dict['y'], self_dict['z'])
                else:
                    if self_dict['orbit_speed'] > 0.0:
                        lat = 0
                        lon = self_dict['orbit_lon']
                    else:
                        lat = random() * 180 - 90
                        lon = random() * 360 - 180
                    self_dict['relative_xyz'] = (
                        self_dict['offset'] * round(cos(lat * pi / 180) * cos(lon * pi / 180), 10),
                        self_dict['offset'] * round(cos(lat * pi / 180) * sin(lon * pi / 180), 10),
                        self_dict['offset'] * round(sin(lat * pi / 180), 10))
                self_dict['xyz'] = (ref_xyz[0] + self_dict['relative_xyz'][0], ref_xyz[1] + self_dict['relative_xyz'][1], ref_xyz[2] + self_dict['relative_xyz'][2])
        # Created cached version
        elif self_dict['xyz'] is None:
            self_dict['root_location'] = self
            self_dict['root_reference'] = None
            self_dict['xyz'] = (self_dict['x'], self_dict['y'], self_dict['z'])
            self_dict['relative_xyz'] = (0.0, 0.0, 0.0)
        if name == 'x':
            return self_dict['xyz'][0]
        if name == 'y':
            return self_dict['xyz'][1]
        if name == 'z':
            return self_dict['xyz'][2]
        if name == 'in_system':
            return self_dict['root_location'].is_system
        return super().__getattribute__(name)

    """ Use the absolute position as the hash """
    def __hash__(self):
        return hash(self.xyz)


Location.set_defaults(Location, __defaults, __tmp_defaults)
