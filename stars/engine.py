import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'kt_exponent': (0.0, 0.0, sys.maxsize),
    'speed_divisor': (0.000001, 0.000001, sys.maxsize),
    'speed_exponent': (0.0, 0.0, sys.maxsize),
    'antimatter_siphon': (0.0, 0.0, sys.maxsize),
}


""" Represent 'an engine' """
class Engine(Defaults):
    """ What is the fastest speed the engine can go without exceeding the tachometer """
    def speed_at_tach_100(self, mass, denials):
        for speed in range(10, 1, -1):
            if self.tachometer(speed, mass, denials) <= 100:
                return speed
        return 1
    
    """ What is the tachometer for the given mass the engine is driving """
    def tachometer(self, speed, mass, denials):
        speed = max(1, int(speed))
        mass = max(0, int(mass))
        denials = max(0, int(denials))
        if denials > 0:
            mass *= speed * (1 - 0.5 ** denials) * 2
        return round((mass ** self.kt_exponent) * (((speed - 1) / self.speed_divisor) ** self.speed_exponent))
    
    """ Calculate how much fuel would be used for a given speed, mass, and distance """
    def fuel_calc(self, speed, mass, denials, ly):
        return (self.tachometer(speed, mass, denials) * mass * ly) + self.siphon_calc(ly)
    
    """ Calculate how much damage is taken for a given speed, mass, and distance """
    def damage_calc(self, speed, mass, ly, num_denials):
        return max(0.0, round((self.tachometer(speed, mass, num_denials) - 100.0) / 2.7) * min(1, ly))
    
    """ How much antimatter is captured for the distance traveled """
    def siphon_calc(self, ly):
        return self.antimatter_siphon * ly


Engine.set_defaults(Engine, __defaults)
