from random import random, randint
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
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'System_' + str(id(self))
        game_engine.register(self)

    """ create planets """
    def _create_system(self, player):
        self.num_planets = round(random() * 5)
        if player:
            if sef.num_planets == 0:
                self.num_planets = 1
        self.planets = []
        planet_args = {
            'reference': 'Planet/' + str(self.name) + "'s " + 'Star',
            'star_system': Reference(self)
            }
        sun = Reference(**planet_args)
        if player:
            sun.radiation = (p.race.hab_radiation_stop+p.race.hab_radiation)/2
        self.planets.append(sun)
        for i in range(self.num_planets):
            if i == 0 and player:
                p = player
                planet_args['player'] = p
                planet_args['gravity'] = (p.race.hab_gravity_stop+p.race.hab_gravity)/2
                planet_args['temperature'] = (p.race.hab_temperature_stop+p.race.hab_temperature)/2
                planet_args['population'] = p.race.starting_pop
                planet_args['power plants'] = p.race.starting_power_plants
                planet_args['facorys'] = p.race.starting_factories
                planet_args['mines'] = p.race.starting_mines
            segment = 100.0 / self.num_planets
            planet_args['reference'] = 'Planet/' + str(self.name) + ' ' + _roman[i]
            planet_args['sun'] = self.planets[0]
            planet_args['distance'] = round(segment * i + randint(5, round(segment)))
            self.planets.append(Reference(**planet_args))
            if i == 0 and player:
                planet_args['player'] = None
                planet_args['gravity'] = None
                planet_args['temperature'] = None
                planet_args['population'] = None
                planet_args['power plants'] = None
                planet_args['facorys'] = None
                planet_args['mines'] = None

        
StarSystem.set_defaults(StarSystem, _defaults)
