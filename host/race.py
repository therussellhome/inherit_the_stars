import to_json

""" Default race values """
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
class Race(to_json.Serializable):
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]

    def __getattribute__(self, name):
        if name in __defaults:
            default = __defaults[name]
            try:
                if type(defaults[name][0]) == type(int):
                    return min([default[1], max([default[2], int(self.__dict__.get(name, default[0]))])])
                elif type(defaults[name][0]) == type(float):
                    return min([default[1], max([default[2], float(self.__dict__.get(name, default[0]))])])
                elif type(defaults[name][0]) == type(bool):
                    return bool(self.__dict__.get(name, default))
            except:
                return default[0]
        else:
            self.__dict__.get(name, None)
