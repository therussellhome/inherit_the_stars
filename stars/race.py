from .defaults import Defaults

""" Default values (default, min, max)  """
__defaults = {
    'growth_rate': [10, 0, 20],
    'gravity_start': [0, 0, 100],
    'gravity_stop': [100, 0, 100],
    'gravity_immune': [False],
    'radiation_start': [0, 0, 100],
    'radiation_stop': [100, 0, 100],
    'radiation_immune': [False],
    'temperature_start': [0, 0, 100],
    'temperature_stop': [100, 0, 100],
    'temperature_immune': [False],
    'population_max': [10000000, 0, 1000000000],
    'effort_efficency': [100, 0, 200],
    'energy_efficency': [100, 0, 200],
    'mine_efficency': [100, 0, 200],
    'factory_efficency': [100, 0, 200]
}

""" Storage class for race parameters """
class Race(Defaults):
    """ Store values but do not load defaults """
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]


Race.set_defaults(Race, __defaults)
