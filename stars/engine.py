import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'kt_exponent': [0.0, 0.0, sys.maxsize],
    'speed_divisor': [0.000001, 0.000001, sys.maxsize],
    'speed_exponent': [0.0, 0.0, sys.maxsize],
    'antimatter_siphon': [0.0, 0.0, sys.maxsize],
}

""" Represent 'a weapon' """
class Engine(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def tachometer(self, speed, mass):
        return (mass ** self.kt_exponent) * ((speed / self.speed_divisor) ** self.speed_exponent)

    def antimatter_siphon(self, ly):
        return self.antimatter_siphon * ly

Engine.set_defaults(Engine, __defaults)
