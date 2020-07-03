from random import random, randint
from . import game_engine
from .defaults import Defaults
from .reference import Reference
from .location import Location


_defaults = {
    'planets': [[]],
    'x': [0, -1000, 1000],
    'y': [0, -1000, 1000],
    'z': [0, -1000, 1000],
    'num_planets': [2, 0, 5]
}

_roman = ["I", "II", "III", "IV", "V"]

class StarSystem(Defaults):
    
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'System_' + str(id(self))
        if 'num_planets' not in kwargs:
            self.num_planets = round(random() * 5)
        if len(self.planets) == 0:
            self._create_system()
        game_engine.register(self)

    """ create planets """
    def _create_system(self):
        self.planets = []
        planet_args = {
            'reference': 'Planet/' + str(self.name) + "'s " + 'Star',
            'star_system': Reference(self)
            }
        sun = Reference(**planet_args)
        self.planets.append(sun)
        for i in range(self.num_planets):
            segment = 100.0 / self.num_planets
            planet_args['reference'] = 'Planet/' + str(self.name) + ' ' + _roman[i]
            planet_args['sun'] = self.planets[0]
            planet_args['distance'] = round(segment * i + randint(5, round(segment)))
            self.planets.append(Reference(**planet_args))

    """ returns the outer system coorenets """
    def get_outer_system(self, location):
        x = (location.x-self.location.x)
        y = (location.y-self.location.y)
        z = (location.z-self.location.z)
        dis = (x**2 + y**2 + z**2)**(1/2)
        x = self.x + (x/dis)*Location.TM_2_LY
        y = self.y + (y/dis)*Location.TM_2_LY
        z = self.z + (z/dis)*Location.TM_2_LY
        return Location('x'=x, 'y'=y, 'z'=z)
    
        
StarSystem.set_defaults(StarSystem, _defaults)
