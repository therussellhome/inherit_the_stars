import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'kt_exponent': [0.0, 0.0, sys.maxsize],
    'speed_divisor': [0.000001, 0.000001, sys.maxsize],
    'speed_exponent': [0.0, 0.0, sys.maxsize],
    'antimatter_siphon': [0.0, 0.0, sys.maxsize],
}

""" Represent 'an engine' """
class Engine(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ What is the tachometer for the given mass the engine is driving """
    def tachometer(self, speed, mass, hyper_denial=False):
        if hyper_denial:
            mass *= speed
        return (mass ** self.kt_exponent) * ((speed / self.speed_divisor) ** self.speed_exponent)

    """ Calculate how much fuel would be used for a given speed, mass, and distance """
    def fuel_check(self, speed, mass, ly, hyper_denial=False):
        return self.tachometer(speed, mass, hyper_denial) * mass * ly

    """ Calculate how much damage is taken for a given speed, mass, and distance """
    def damage_check(self, speed, mass, ly, hyper_denial=False):
        #TODO play test this number
        return max(0.0, self.tachometer(speed, mass, hyper_denial) - 100.0) * ly

    """ How much antimatter is captured for the distance traveled """
    def antimatter_siphon(self, ly):
        return self.antimatter_siphon * ly

Engine.set_defaults(Engine, __defaults)
