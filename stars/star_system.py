from random import random, randint
from . import game_engine
from .defaults import Defaults
from .reference import Reference
from .location import Location


__defaults = {
    'planets': [[]],
    'location': [Location()],
    'num_planets': [2, 0, 5]
}

_roman = ["I", "II", "III", "IV", "V"]

class StarSystem(Defaults):
    
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'System ' + str(id(self))
        game_engine.register(self)

    """ create planets """
    def create_system(self, player):
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

    """ returns the outer system coorenets """
    def get_outer_system(self, location):
        x = (location.x-self.location.x)
        y = (location.y-self.location.y)
        z = (location.z-self.location.z)
        dis = (x**2 + y**2 + z**2)**(1/2)
        dis = self.location - location
        x = self.x + (x/dis)*stars_math.TERAMETER_2_LIGHTYEAR
        y = self.y + (y/dis)*stars_math.TERAMETER_2_LIGHTYEAR
        z = self.z + (z/dis)*stars_math.TERAMETER_2_LIGHTYEAR
        return Location(x=x, y=y, z=z)
        
StarSystem.set_defaults(StarSystem, __defaults)
