from .defaults import Defaults

__defaults = {
    'name': ['kill all'],
    '1st_target': ['any'],
    'options_1st_target': ['any', 'starbace', 'ship', 'disengage'],
    '2nd_target': ['any'],
    'options_2nd_target': ['any', 'starbace', 'ship', 'disengage'],
    'tactic': ['max damage'],
    'options_tactic': ['max damage', 'max damage ratio', 'max net damage', 'min damage to self', 'run away'],
    'work alone': [False],
}

class BattlePlan(Defaults):
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]

BattlePlan.set_defaults(BattlePlan, __defaults)
