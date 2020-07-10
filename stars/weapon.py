import sys
from . import stars_math
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'power': [0, 0, sys.maxsize],
    'armor_multiplier': [0, 0, 200],
    'is_beam': [True],
    'is_multishot': [False],
    'range': [0.0, 0.0, sys.maxsize], # terameters
    'accuracy': [100, 0, 100]
}

""" Represent 'a weapon' """
class Weapon(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Get the accuracy of the weapon at a given range """
    def get_accuracy(self, target_ly):
        range_ly = self.range * stars_math.TERAMETER_2_LIGHTYEAR 
        if not self.is_beam:
            return self.accuracy * (1 - (target_ly / range_ly) ** 4)
        return self.accuracy

    """ Get the power at a given range for a given shield and armor """
    def get_power(self, target_ly, shield, armor):
        range_ly = self.range * stars_math.TERAMETER_2_LIGHTYEAR 
        if target_ly < range_ly:
            power = self.power
            if self.is_beam:
                power = self.power * (1 - target_ly / range_ly)
            if power > shield:
                power = shield + (power - shield) * self.armor_multiplier
            return power
        return 0.0

    """ Calculate the damage of firing the weapon at a ship """
    def get_damage(self, target_ly, shield, armor, visible_ly, ecm):
        if self.get_accuracy(target_ly) * (1.0 + visible_ly / 2000.0) - ecm * 100 * (target_ly ** 0.5) <= randint(0, 100):
            return 0
        return self.get_power(target_ly, shield, armor)

Weapon.set_defaults(Weapon, __defaults)
