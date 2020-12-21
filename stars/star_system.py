from random import random, randint
from . import game_engine
from .defaults import Defaults
from .reference import Reference
from .location import Location
from .sun import Sun
from .planet import Planet
from .cargo import Cargo


__defaults = {
    'planets': [[]],
    'location': [Location()],
}

_roman = ["I", "II", "III", "IV", "V"]

""" Star System with its planets """
class StarSystem(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'System ' + str(id(self))
        game_engine.register(self)

    """ create planets """
    def create_system(self, player=None):
        planet_args = {
            'name': self.name + "'s " + 'Star',
            'star_system': Reference(self),
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
        self.planets.append(Sun(**planet_args))
        for i in range(num_planets):
            segment = 100.0 / num_planets
            planet_args['name'] = self.name + ' ' + _roman[i]
            planet_args['distance'] = round(segment * i + randint(5, round(segment)))
            self.planets.append(Planet(**planet_args))
        if player:
            self.planets[home].gravity = (player.race.hab_gravity_stop + player.race.hab_gravity) / 2
            self.planets[home].temperature = (player.race.hab_temperature_stop + player.race.hab_temperature) / 2
            self.planets[home].colonize(player)
            self.planets[home].on_surface.population = player.race.starting_colonists

    """ get the sun for the system """
    def sun(self):
        if len(self.planets) > 0:
            return self.planets[0]
        return None

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
    
    """ sweeps mines """
    def sweep_mines(self, power, shot_factor, wep_range, field):
        return round(power * shot_factor * (wep_range * 10) ** 3 * self.mines[field] / 65000000000000000 * 100 * 20000000)
    
    """ uses the mine decay formula"""    
    def mines_decay(self):
        g = 0
        for planet in self.planets:
            g += planet.gravity ** 2
        for key in self.mines:
            p_cap = self.mines[key] / 65000000000000000
            print(self.mines[key])
            self.mines[key] -= round(g * (p_cap ** 3) * 10000000000 + p_cap * 0.015 * 65000000000000000)
            print(self.mines[key])
    
    """ finds the number of mines hit for a given mass of ship and distance travled """
    def mines_hit(self, mass, distance, field):
        return round((3.14159 * mass ** 2) * distance * (self.mines[field] / (4 / 3 * 3.14159 * 100 ** 3)))
    
    """ planets/suns sorted by habitability (exclude already colonized) """
    def get_colonizable_planets(self, race):
        pass
        """
        planets = []
        if race.primary_race_trait == 'Pa\'anuri':
            if not self.planets[0].is_colonized:
                planets.append(self.planets[0])
        else:
            for p in self.planets[1:]:
                if not p.is_colonized:
        """


StarSystem.set_defaults(StarSystem, __defaults)
