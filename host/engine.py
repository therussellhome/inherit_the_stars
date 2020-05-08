import sys
import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'kt_exponent': [1.5, 0.0, sys.maxsize],
    'speed_divisor': [12.68, 0.0, sys.maxsize],
    'speed_exponent': [5.0, 0.0, sys.maxsize],
    'generation': [0, 0, sys.maxsize]
}

""" Represent 'ship engine' """
class Engine(game_engine.Defaults):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

    """ Calculate the efficency of the engine """
    def calc_efficency(self, speed, mass):
        return (mass ** self.kt_exponent) * (((speed - 1) / self.speed_divisor ) ** self.speed_exponent)

    """ Calculate fuel generation """
    def calc_fuel_generation(self, speed):
        return speed * self.generate

# Register the class with the game engine
game_engine.register(Engine, defaults=__defaults)
