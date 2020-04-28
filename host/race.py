import game_engine

""" Default race values """
_defaults = {
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
class Race:
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]

    def __getattribute__(self, name):
        if name in _defaults:
            default = _defaults[name]
            try:
                value = object.__getattribute__(self, name)
                if type(defaults[name][0]) == type(int):
                    return min([default[1], max([default[2], int(value)])])
                elif type(defaults[name][0]) == type(float):
                    return min([default[1], max([default[2], float(value)])])
                elif type(defaults[name][0]) == type(bool):
                    return bool(value)
            except:
                return default[0]
        else:
            return object.__getattribute__(self, name)

# Register the class with the game engine
game_engine.register_class(Race)
