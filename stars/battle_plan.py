from .defaults import Defaults
from . import stars_math

__defaults = {
    'name': ['kill all'],
    'p_target': ['any'],
    's_target': ['any'],
    'standoff': [0.0, 0.0, 1.0],
    'wait_until_closed_to_fire': [False],
}

class BattlePlan(Defaults):
    options_p_target = ['any', 'starbase', 'ship', 'disengage']
    options_s_target = ['any', 'starbase', 'ship', 'disengage']
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.p_target not in BattlePlan.options_p_target:
            self.s_target = BattlePlan.options_p_target[0]
        if self.p_target not in BattlePlan.options_s_target:
            self.s_target = BattlePlan.options_s_target[0]

BattlePlan.set_defaults(BattlePlan, __defaults)
