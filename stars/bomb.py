import sys
from random import randint
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'percent_pop_kill': (0.0, 0.0, 100.0),
    'minimum_pop_kill': (0, 0, sys.maxsize),
    'shield_kill': (0, 0, sys.maxsize),
    'max_defense': (100, 1, 1000),
    'dirty_temperature': (0.0, -1.0, 1.0),
    'dirty_radiation': (0.0, -1.0, 1.0),
    'dirty_gravity': (0.0, -1.0, 1.0),
}


""" Represent 'a bomb' """
class Bomb(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Calculate the adjustment for the max defense to put 0 shields at 0 defense
        self.__cache__['zero_zero_adjustment'] = 500.0 / self.max_defense

    """ Based on a population and shield, calculate the percent chance the bomb will get through """
    def percent_defense(self, population, shield_strength):
        return self.max_defense - 500.0 / (shield_strength / population + self.__cache__['zero_zero_adjustment'])


Bomb.set_defaults(Bomb, __defaults)
