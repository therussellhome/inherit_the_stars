from .defaults import Defaults

__defaults = {
    'name': ['kill all'],
    'p_target': ['any'],
    'options_p_target': ['any', 'starbase', 'ship', 'disengage'],
    's_target': ['any'],
    'options_s_target': ['any', 'starbase', 'ship', 'disengage'],
    'close_to': [0, 0, 0.60],
    'work_alone': [False],
    'wait_until_closed_to_fire': [False],
}

class BattlePlan(Defaults):
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]

BattlePlan.set_defaults(BattlePlan, __defaults)
