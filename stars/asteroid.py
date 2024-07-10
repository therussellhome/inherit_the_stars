from .defaults import Defaults
from .location import Location
from .reference import Reference
from .minerals import Minerals, MINERAL_TYPES
import sys
from math import floor, pi


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
    'minerals': Minerals(),
    'location': Location(),
    'ke': (0, 0, sys.maxsize),
    'target': Location(),
    'player': Reference('Player'),
    'decay_factor': (0.01, 0.0, 1.0),
    'away': False
}

""" Represent 'asteroid' """
class Asteroid(Defaults):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in kwargs:
            if name in MINERAL_TYPES:
                self.minerals[name] += kwargs[name]
        if self.mass == 0:
            pass #TODO delete

    def __getattribute__(self, name):
        if name == 'mass':
            return self.minerals.sum()
        return super().__getattribute__(name)

    def get_speed(self):
        if self.mass == 0:
            return 0
        v = (2 * self.ke / self.mass) ** 0.5
        hyper = floor(v ** 0.5)
        return hyper

    def move(self):
        distance = self.location - self.target
        max_distance = self.get_speed() ** 2
        if distance < max_distance and not self.target.reference and not self.away:
            self.away = True
            max_distance = max_distance - distance
            self.location = self.target.move(self.location, max_distance, self.away)
        else:
            self.location = self.location.move(self.target, max_distance, self.away)

    def impact(self):
        if not self.location == self.target:
            return
        if self.location.reference ^ 'Planet' or self.location.reference ^ 'Sun':
            planet = self.location.reference
            planet.catch_packet(self)

    def decay(self):
        if self.player
            if player.race.primay_race_trait == 'TANSTAAFL':
                self.ke *= (1 - (self.decay_factor * (2/3)))
            else:
                self.ke *= (1 - self.decay_factor)

    def scan_penetrating(self):
        if self.player and player.race.primay_race_trait == 'TANSTAAFL':
            radius = (3.0 / 4.0 / pi * (self.player.tech_level.electronics + 1.0) / 3.0) ** (1.0 / 3.0)
            if self.player.race.lrt_2ndSight:
                radius *= 2.5
            scan.penetrating(self.player, self.location, radius)
    

Asteroid.set_defaults(Asteroid, __defaults)
#ke -= ke * decay_factor


#what does it need to have?
#minerals is class
#location is class
#mass
#ke is kenetic energy.
#target is location
#player (only if TANSTAAFL) is reference
#decay rate

#from what does it inherit
#buildable
#not minerals (it has minerals)
