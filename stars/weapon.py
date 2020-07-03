import sys
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

    def get_power(self, target_range, shield, armor):
        if target_range < self.range:
            power = self.power
            if self.is_beam:
                power = self.power * (1 - target_range / self.range)
            if power > shield:
                power = shield + (power - shield) * self.armor_multiplier
            return power
        return 0.0

    def get_accuracy(self, target_range):
        if not self.is_beam:
            return self.accuracy * (1 - (target_range / self.accuracy) ** 4)
        return self.accuracy

Weapon.set_defaults(Weapon, __defaults)
