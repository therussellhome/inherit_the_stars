from random import randint
from . import game_engine
from .defaults import Defaults
from .reference import Reference

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
        super()._apply_defaults(**kwargs)
        if 'name' not in kwargs:
            self.name = 'System_' + str(id(self))
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
        segment = 100.0 / self.num_planets
        for i in range(self.num_planets):
            planet_args['reference'] = 'Planet/' + str(self.name) + ' ' + _roman[i]
            planet_args['sun'] = self.planets[0]
            planet_args['distance'] = round(segment * i + randint(5, segment))
            self.planets.append(Reference(**planet_args))
    
        
StarSystem.set_defaults(StarSystem, _defaults)
