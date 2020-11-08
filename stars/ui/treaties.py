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
    'cost_p1_to_p2_fuel': [10, 0, maxsize],
    'p1_is_selling_fuel': [False],
    'cost_p2_to_p1_fuel': [10, 0, maxsize],
    'p2_is_selling_fuel': [False],
    'cost_p1_to_p2_stargate': [5000, 0, maxsize],
    'p1_is_selling_stargate': [False],
    'cost_p2_to_p1_stargate': [5000, 0, maxsize],
    'p2_is_selling_stargate': [False],
    'shared_p1_general_intel': [False],
    'p1_to_p2_safe_passage': [False],
    'shared_p2_general_intel': [False],
    'p2_to_p1_safe_passage': [False],
    'stautus': ['']
}

class Treaty(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __sub__(self, other):
        k1 = ['p1', 'p1_to_p2_safe_passage', 'shared_p1_general_intel', 'p1_is_selling_stargate', 'cost_p1_to_p2_stargate', 'p1_is_selling_fuel', 'cost_p1_to_p2_fuel', 'p1_is_selling_lithium', 'cost_p1_to_p2_lithium', 'p1_is_selling_silicon', 'cost_p1_to_p2_titanium', 'p1_is_selling_titanium', 'cost_p1_to_p2_silicon']
        k2 = ['p2', 'p2_to_p1_safe_passage', 'shared_p2_general_intel', 'p2_is_selling_stargate', 'cost_p2_to_p1_stargate', 'p2_is_selling_fuel', 'cost_p2_to_p1_fuel', 'p2_is_selling_lithium', 'cost_p2_to_p1_lithium', 'p2_is_selling_silicon', 'cost_p2_to_p1_titanium', 'p2_is_selling_titanium', 'cost_p2_to_p1_silicon']
        treaty = Treaty()
        if self.relation == other.relation:
            treaty.relation = self.relation
        treaty.stautus = 'received'
        for key in k1:
            treaty.key = self.key
        for key in k2:
            treaty.key = other.key
        return treaty

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

Treaty.set_defaults(Treaty, __defaults, no_reset=['p2', 'p1'])
