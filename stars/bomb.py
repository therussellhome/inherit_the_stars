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

    """ Calculate the number of shield facilities to kill """
    def kill_shield_facilities(self, population, shield_strength):
        if self.percent_defense(population, shield_strength) >= randint(0, 100):
            return 0
        return self.shield_kill / 100

    """ Calculate the number of colonists to kill """
    def kill_population(self, population, shield_strength):
        if self.percent_defense(population, shield_strength) >= randint(0, 100):
            return 0
        return max(self.minimum_pop_kill / 100, self.percent_pop_kill / 100 * population)


Bomb.set_defaults(Bomb, __defaults)
