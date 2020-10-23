from ..defaults import Defaults
from .. import game_engine
from sys import maxsize

__defaults = {
    'p1': [''],
    'p2': [''],
    'relation': ['nutral'],
    'options_relation': [['team', 'nutral', 'enemy']],
    'cost_p1_to_p2_titanium': [100, 0, maxsize],
    'p1_is_selling_titanium': [False],
    'cost_p2_to_p1_titanium': [100, 0, maxsize],
    'p2_is_selling_titanium': [False],
    'cost_p1_to_p2_silicon': [100, 0, maxsize],
    'p1_is_selling_silicon': [False],
    'cost_p2_to_p1_silicon': [100, 0, maxsize],
    'p2_is_selling_silicon': [False],
    'cost_p1_to_p2_lithium': [100, 0, maxsize],
    'p1_is_selling_lithium': [False],
    'cost_p2_to_p1_lithium': [100, 0, maxsize],
    'p2_is_selling_lithium': [False],
    'cost_p1_to_p2_fuel': [5, 0, maxsize],
    'p1_is_selling_fuel': [False],
    'cost_p2_to_p1_fuel': [5, 0, maxsize],
    'p2_is_selling_fuel': [False],
    'cost_p1_to_p2_stargate': [5000, 0, maxsize],
    'p1_is_selling_stargate': [False],
    'cost_p2_to_p1_stargate': [5000, 0, maxsize],
    'p2_is_selling_stargate': [False],
    'shared_p1_general_intel': [False],
    'p1_to_p2_safe_passage': [False],
    'shared_p2_general_intel': [False],
    'p2_to_p1_safe_passage': [False],
    'stautus': ['how to calculate this? hmmm']
}

class Treaty(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def post(self, action):
        if action == 'revoc':
            self.relation = 'enemy'
        if action == 'propose':
            game_engine.send_message(self.p1, self.p2, 'do you except ' + p1.name + '\'s treaty proposal?')
        if self.relation == 'enemy':
            for key in self.__dict__:
                self.__dict__[key] = False
        pass

Treaty.set_defaults(Treaty, __defaults)
