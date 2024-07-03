improt math
from .defaults import Defaults
from .location import Location
from .reference import Reference
from .minerals import Minerals
import sys


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
        if 'lithium' in kwargs:
            self.minerals.lithium += kwargs['lithium']
        if 'titanium' in kwargs:
            self.minerals.titanium += kwargs['titanium']
        if 'silicon' in kwargs:
            self.minerals.silicon += kwargs['silicon']
        if self.minerals.sum() == 0:
            pass #TODO delete

    def get_speed(self):
        mass = self.minerals.sum()
        v = (2 * self.ke / mass) ** 0.5
        hyper = math.floor(v ** 0.5)
        return hyper

    def move(self):
        distance = self.locaiton - self.target
        max_distance = self.get_speed() ** 2
        if distance < max_distance and not self.target.reference and not self.away:
            self.away = True
            max_distance = max_distance - distance
            self.location = self.target.move(self.location, max_distance, self.away)
        else:
            self.location = self.location.move(self.target, max_distance, self.away)

    def impact(self):
        pass
    

Asteroid.set_defaults(Asteroid, __defaults)
#ke -= ke * decay_factor


#what does it need to have?
#minerals is class
#location is class
#mass
#speed is hyper
#target is location
#player (only if TANSTAAFL) is reference
#decay rate

#from what does it inherit
#buildable
#not minerals (it has minerals)
