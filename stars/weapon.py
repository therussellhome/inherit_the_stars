import sys
from . import stars_math
from .defaults import Defaults
from random import randint


""" Default values (default, min, max)  """
__defaults = {
    'power': (0, 0, sys.maxsize),
    'armor_multiplier': (1, 0, 200),
    'is_beam': True,
    'is_multishot': False,
    'range_tm': (0.0, 0.0, sys.maxsize), # terameters
    'accuracy': (100, 0, 200),
}

""" Represent 'a weapon' """
class Weapon(Defaults):
    """ Get the accuracy of the weapon at a given range """
    def get_accuracy(self, target_ly):
        range_ly = self.range_tm * stars_math.TERAMETER_2_LIGHTYEAR 
        if not self.is_beam:
            return self.accuracy * (1 - (target_ly / range_ly) ** 4)
        return self.accuracy

    """ Get the power at a given range for a given shield and armor """
    def get_power(self, target_ly, shield, armor):
        range_ly = self.range_tm * stars_math.TERAMETER_2_LIGHTYEAR 
        if target_ly < range_ly:
            power = self.power
            power_to_armor = 0
            if self.is_beam:
                power = self.power * (1 - target_ly / range_ly)
            if not self.is_beam:
                difference = int(power/4)
                power -= difference
                power_to_armor += difference
            power_to_shield = min(power, shield)
            power_to_armor += max((power - shield) * self.armor_multiplier, 0)
            return (power_to_shield, power_to_armor)
        return (0, 0)

    """ Calculate the damage of firing the weapon at a ship """
    def get_damage(self, target_ly, shield, armor, visible_ly, ecm):
        #print(self.get_accuracy(target_ly) * (1.0 + visible_ly / 2000.0) - ecm * 100 * (target_ly ** 0.5))
        if self.get_accuracy(target_ly) * (1.0 + visible_ly / 2000.0) - ecm * 100 * (target_ly ** 0.5) <= randint(0, 100):
            return (0, 0)
        damage = self.get_power(target_ly, shield, armor)
        return (damage[0], damage[1])


Weapon.set_defaults(Weapon, __defaults)
