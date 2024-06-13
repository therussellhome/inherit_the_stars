import sys
from random import random, randint
from . import game_engine
from . import stars_math
from .defaults import Defaults
from .reference import Reference
from .location import Location
from .sun import Sun
from .planet import Planet
from .cargo import Cargo


__defaults = {
    'ID': '@UUID',
    'planets': [],
    'location': Location(),
    'minefield': (0, 0, sys.maxsize),
    'minefield_owner': Reference('Player'),
}


_roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']


""" Star System with its planets """
class StarSystem(Defaults):
    """ Initialize defaults """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        game_engine.register(self)

    """ create planets """
    def create_system(self, race=None, num_planets=-1):
        planet_args = {
            'ID': self.ID + "'s " + 'Star',
            'star_system': Reference(self),
            'radiation': randint(0, 100),
            'gravity': 'generate',
            'temperature': 'generate',
        }
        if num_planets < 0:
            num_planets = round(random() * 5)
        home = -1
        if race:
            planet_args['radiation'] = int((race.hab_radiation_stop + race.hab_radiation) / 2)
            if race.primary_race_trait == 'Pa\'anuri':
                num_planets = max(1, num_planets)
                home = 0
                planet_args['gravity'] = int((race.hab_gravity_stop + race.hab_gravity) / 2)
                planet_args['temperature'] = int((race.hab_temperature_stop + race.hab_temperature) / 2)
            else:
                num_planets = max(2, num_planets)
                home = randint(1, num_planets)
        self.planets.append(Sun(**planet_args))
        for i in range(num_planets):
            segment = 100.0 / num_planets
            planet_args['ID'] = self.ID + ' ' + _roman[i]
            planet_args['distance'] = round(segment * i + randint(5, round(segment)))
            planet_args['gravity'] = 'generate'
            planet_args['temperature'] = 'generate'
            if i != home - 1:
                self.planets.append(Planet(**planet_args))
            else:
                planet_args['gravity'] = int((race.hab_gravity_stop + race.hab_gravity) / 2)
                planet_args['temperature'] = int((race.hab_temperature_stop + race.hab_temperature) / 2)
                self.planets.append(Planet(**planet_args, homeworld=True))
                planet_temp = round((100 - self.planets[home].distance) * 0.35 + self.sun().temperature * 0.65)
                if planet_temp - self.planets[home].temperature not in range(-15, 15):
                    self.sun()['temperature'] = round(((self.planets[home].temperature) - ((100 - self.planets[home].distance) * 0.35)) / 0.65)
                    for pi in range(1, len(self.planets)-1):
                        planet = self.planets[pi]
                        planet_temp = round((100 - planet.distance) * 0.35 + self.sun().temperature * 0.65)
                        if planet.temperature - planet_temp not in range(-15, 15):
                            planet.temperature = planet_temp + randint(-15, 15)
        if race:
            return Reference(self.planets[home])
        return None

    """ get the sun for the system """
    def sun(self):
        if len(self.planets) > 0:
            return self.planets[0]
        return None

    """ returns the outer system coorenets """
    def get_outer_system(self, location):
        #TODO is anyone actually using this?
        x = (location.x-self.location.x)
        y = (location.y-self.location.y)
        z = (location.z-self.location.z)
        dis = (x**2 + y**2 + z**2)**(1/2)
        dis = self.location - location
        x = self.location.x + (x/dis)*stars_math.TERAMETER_2_LIGHTYEAR
        y = self.location.y + (y/dis)*stars_math.TERAMETER_2_LIGHTYEAR
        z = self.location.z + (z/dis)*stars_math.TERAMETER_2_LIGHTYEAR
        return Location(x=x, y=y, z=z)

    """ Lay mines """
    def lay_mines(self, quantity, player):
        #TODO check treaty as non-teammate mines should function as mine sweeping
        #TODO update test to match when you update the function
        #TODO make this match sweep_mines, mines_decay, and mines_hit
        if not self.minefield_owner:
            self.minefield_owner = Reference(player)
        self.minefield += quantity

    """ sweeps mines """
    def sweep_mines(self, power, shot_factor, wep_range, field):
        return round(power * shot_factor * (wep_range * 10) ** 3 * self.mines[field] / 65000000000000000 * 100 * 20000000)
    
    """ uses the mine decay formula"""    
    def mines_decay(self):
        g = 0
        for planet in self.planets:
            g += planet.gravity ** 2
        for key in self.mines:
            p_cap = self.mines[key] / 65000000000000000 # TODO this number seem like it should move to a constant
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
