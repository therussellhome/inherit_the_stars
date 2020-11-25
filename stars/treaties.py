from .defaults import Defaults
#from . import game_engine
from sys import maxsize

__defaults = {
    'p1': [''],
    'p2': [''],
    'relation': ['neutral'],
    #'options_relation': [['team', 'neutral', 'enemy']],
    'cost_p1_to_p2_titanium': [33, 0, 120],
    'p1_is_selling_titanium': [False],
    'cost_p2_to_p1_titanium': [33, 0, 120],
    'p2_is_selling_titanium': [False],
    'cost_p1_to_p2_silicon': [33, 0, 120],
    'p1_is_selling_silicon': [False],
    'cost_p2_to_p1_silicon': [33, 0, 120],
    'p2_is_selling_silicon': [False],
    'cost_p1_to_p2_lithium': [33, 0, 120],
    'p1_is_selling_lithium': [False],
    'cost_p2_to_p1_lithium': [33, 0, 120],
    'p2_is_selling_lithium': [False],
    'cost_p1_to_p2_fuel': [10, 0, 999],
    'p1_is_selling_fuel': [False],
    'cost_p2_to_p1_fuel': [10, 0, 999],
    'p2_is_selling_fuel': [False],
    'cost_p1_to_p2_stargate': [5000, 0, 99999],
    'p1_is_selling_stargate': [False],
    'cost_p2_to_p1_stargate': [5000, 0, 99999],
    'p2_is_selling_stargate': [False],
    'p1_is_selling_intel': [False],
    'cost_p2_to_p1_intel': [100, 0, 999],
    'p2_is_selling_intel': [False],
    'cost_p1_to_p2_intel': [100, 0, 999],
    'p1_is_selling_passage': [False],
    'cost_p2_to_p1_passage': [50, 0, 999],
    'p2_is_selling_passage': [False],
    'cost_p1_to_p2_passage': [50, 0, 999],
    'status': ['']
}

class Treaty(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def merge(self, other):
        other = other.flip()
        k1 = ['p1', 'p1_to_p2_safe_passage', 'shared_p1_general_intel', 'p1_is_selling_stargate', 'cost_p1_to_p2_stargate', 'p1_is_selling_fuel', 'cost_p1_to_p2_fuel', 'p1_is_selling_lithium', 'cost_p1_to_p2_lithium', 'p1_is_selling_silicon', 'cost_p1_to_p2_titanium', 'p1_is_selling_titanium', 'cost_p1_to_p2_silicon']
        k2 = ['p2', 'p2_to_p1_safe_passage', 'shared_p2_general_intel', 'p2_is_selling_stargate', 'cost_p2_to_p1_stargate', 'p2_is_selling_fuel', 'cost_p2_to_p1_fuel', 'p2_is_selling_lithium', 'cost_p2_to_p1_lithium', 'p2_is_selling_silicon', 'cost_p2_to_p1_titanium', 'p2_is_selling_titanium', 'cost_p2_to_p1_silicon']
        treaty = Treaty()
        if self.relation == other.relation:
            treaty.relation = self.relation
        treaty.status = 'received'
        for key in k1:
            treaty.__dict__[key] = self.__dict__[key]
            print(treaty.__dict__[key])
        for key in k2:
            treaty.__dict__[key] = other.__dict__[key]
            print(treaty.__dict__[key])
        return (treaty, treaty.flip())

    def flip(self):
        t = Treaty()
        t.p1 = self.p2
        t.p2 = self.p1
        t.cost_p1_to_p2_titanium = self.cost_p2_to_p1_titanium
        t.p1_is_selling_titanium = self.p2_is_selling_titanium
        t.cost_p2_to_p1_titanium = self.cost_p1_to_p2_titanium
        t.p2_is_selling_titanium = self.p1_is_selling_titanium
        t.cost_p1_to_p2_silicon = self.cost_p2_to_p1_silicon
        t.p1_is_selling_silicon = self.p2_is_selling_silicon
        t.cost_p2_to_p1_silicon = self.cost_p1_to_p2_silicon
        t.p2_is_selling_silicon = self.p1_is_selling_silicon
        t.cost_p1_to_p2_lithium = self.cost_p2_to_p1_lithium
        t.p1_is_selling_lithium = self.p2_is_selling_lithium
        t.cost_p2_to_p1_lithium = self.cost_p1_to_p2_lithium
        t.p2_is_selling_lithium = self.p1_is_selling_lithium
        t.cost_p1_to_p2_fuel = self.cost_p2_to_p1_fuel
        t.p1_is_selling_fuel = self.p2_is_selling_fuel
        t.cost_p2_to_p1_fuel = self.cost_p1_to_p2_fuel
        t.p2_is_selling_fuel = self.p1_is_selling_fuel
        t.cost_p1_to_p2_stargate = self.cost_p2_to_p1_stargate
        t.p1_is_selling_stargate = self.p2_is_selling_stargate
        t.cost_p2_to_p1_stargate = self.cost_p1_to_p2_stargate
        t.p2_is_selling_stargate = self.p1_is_selling_stargate
        t.p1_is_selling_intel = self.p2_is_selling_intel
        t.cost_p2_to_p1_intel = self.cost_p1_to_p2_intel
        t.p2_is_selling_intel = self.p1_is_selling_intel
        t.cost_p1_to_p2_intel = self.cost_p2_to_p1_intel
        t.p1_is_selling_passage = self.p2_is_selling_passage
        t.cost_p2_to_p1_passage = self.cost_p1_to_p2_passage
        t.p2_is_selling_passage = self.p1_is_selling_passage
        t.cost_p1_to_p2_passage = self.cost_p2_to_p1_passage
        t.relation = self.relation
        t.status = self.status
        #self.__dict__ = t.__dict__
        return t
    
    """ Equality check """
    def __eq__(self, other):
        #k1 = ['p1', 'p1_to_p2_safe_passage', 'shared_p1_general_intel', 'p1_is_selling_stargate', 'cost_p1_to_p2_stargate', 'p1_is_selling_fuel', 'cost_p1_to_p2_fuel', 'p1_is_selling_lithium', 'cost_p1_to_p2_lithium', 'p1_is_selling_silicon', 'cost_p1_to_p2_titanium', 'p1_is_selling_titanium', 'cost_p1_to_p2_silicon']
        #k2 = ['p2', 'p2_to_p1_safe_passage', 'shared_p2_general_intel', 'p2_is_selling_stargate', 'cost_p2_to_p1_stargate', 'p2_is_selling_fuel', 'cost_p2_to_p1_fuel', 'p2_is_selling_lithium', 'cost_p2_to_p1_lithium', 'p2_is_selling_silicon', 'cost_p2_to_p1_titanium', 'p2_is_selling_titanium', 'cost_p2_to_p1_silicon']
        #a = [self.relation == other.relation]
        #for i in range(len(k1)):
        #    key1 = k1[i]
        #    key2 = k2[i]
        #    a.append((self.__dict__[key1] == other.__dict__[key1] and self.__dict__[key2] == other.__dict__[key2]))# or (self.key1 == other.key2 and self.key2 = other.key1))
        #    #print(self.__dict__[key1], other.__dict__[key1], key1)
        #    #print(self.__dict__[key2], other.__dict__[key2], key2)
        #    #print(a)
        #print('sometings not right...,,,')
        return self.__dict__ == other.__dict__

Treaty.set_defaults(Treaty, __defaults, no_reset=['p2', 'p1'])
