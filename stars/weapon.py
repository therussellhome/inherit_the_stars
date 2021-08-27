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
        if target_ly >= range_ly:
            return 0
        elif not self.is_beam:
            return self.accuracy * (1 - (target_ly / range_ly) ** 4)
        return self.accuracy

    """ Get the power at a given range for a given shield and armor """
    def get_power(self, target_ly, shield, armor):
        range_ly = self.range_tm * stars_math.TERAMETER_2_LIGHTYEAR 
        if target_ly < range_ly:
            power = self.power
            power_to_armor = 0
            if self.is_beam:
                # attenuate beam power by range
                power = round(self.power * (1 - target_ly / range_ly))
                to_shield = min(power, shield)
            else:
                # 25% of missile power is direct to armor
                to_shield = min(round(power * 0.75), shield)
            return (to_shield, (power - to_shield) * self.armor_multiplier)
        return (0, 0)

    """ Calculate the damage of firing the weapon at a ship """
    def get_damage(self, target_ly, shield, armor, visible_ly, ecm):
        #print(self.get_accuracy(target_ly) * (1.0 + visible_ly / 2000.0) - ecm * 100 * (target_ly ** 0.5))
        if self.get_accuracy(target_ly) * (1.0 + visible_ly / 2000.0) - ecm * 100 * (target_ly ** 0.5) <= randint(0, 100):
            return (0, 0)
        return self.get_power(target_ly, shield, armor)


Weapon.set_defaults(Weapon, __defaults)
