from . import game_engine
from random import randint
from random import random

_defaults = {
    'planets': [[]],
    'x': [0, -1000, 1000],
    'y': [0, -1000, 1000],
    'z': [0, -1000, 1000],
    'num_planets': [2, 0, 5]
}

_roman = ["I", "II", "III", "IV", "V"]

class StarSystem(game_engine.Defaults):
    
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)
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
            'star_system': game_engine.Reference(self)
            }
        sun = game_engine.Reference(**planet_args)
        self.planets.append(sun)
        for i in range(self.num_planets):
            segment = 100.0 / self.num_planets
            planet_args['reference'] = 'Planet/' + str(self.name) + ' ' + _roman[i]
            planet_args['sun'] = self.planets[0]
            planet_args['distance'] = round(segment * i + randint(5, round(segment)))
            self.planets.append(game_engine.Reference(**planet_args))
    
        

# Register the class with the game engine
game_engine.register(StarSystem, defaults=_defaults)
