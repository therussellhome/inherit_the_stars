from random import random, randint
from .defaults import Defaults
from .reference import Reference
from .location import Location
from .sun import Sun
from .planet import Planet


__defaults = {
    'planets': [[]],
    'location': [Location()],
    'num_planets': [2, 0, 5]
}

_roman = ["I", "II", "III", "IV", "V"]

""" Star System with its planets """
class StarSystem(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'System ' + str(id(self))

    """ create planets """
    def create_system(self, player=None):
        planet_args = {
            'name': self.name + "'s " + 'Star',
            'star_system': Reference(self)
        }
        num_planets = round(random() * 5)
        if player:
            planet_args['radiation'] = (player.race.hab_radiation_stop + player.race.hab_radiation) / 2
            if player.race.primary_race_trait == 'Pa\'anuri':
                num_planets = max(1, num_planets)
                home = 0
            else:
                num_planets = max(2, num_planets)
                home = randint(1, num_planets)
        sun = Sun(**planet_args)
        self.planets.append(Reference(sun))
        planet_args['sun'] = self.planets[0]
        for i in range(num_planets):
            segment = 100.0 / num_planets
            planet_args['name'] = self.name + ' ' + _roman[i]
            planet_args['distance'] = round(segment * i + randint(5, round(segment)))
            p = Planet(**planet_args)
            self.planets.append(Reference(p))
        if player:
            self.planets[home].gravity = (player.race.hab_gravity_stop + player.race.hab_gravity) / 2
            self.planets[home].temperature = (player.race.hab_temperature_stop + player.race.hab_temperature) / 2
            self.planets[home].colonize(player, None, player.race.starting_pop, player.race.starting_factories)
            self.planets[home].power_plants = player.race.starting_power_plants
            self.planets[home].mines = player.race.starting_mines

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
