from .defaults import Defaults
#from . import game_engine
from sys import maxsize
from .reference import Reference

__defaults = {
    'me': [Reference],
    'other_player': [Reference()],
    'relation': ['neutral'],
    'accepted_by': [[]],
    'rejected_by': [[]],
    'replaced_by': [[]],
    'sell_ti_at': [33, 0, 120],
    'sell_ti': [False],
    'buy_ti_at': [33, 0, 120],
    'buy_ti': [False],
    'sell_si_at': [33, 0, 120],
    'sell_si': [False],
    'buy_si_at': [33, 0, 120],
    'buy_si': [False],
    'sell_li_at': [33, 0, 120],
    'sell_li': [False],
    'buy_li_at': [33, 0, 120],
    'buy_li': [False],
    'sell_fuel_at': [10, 0, 999],
    'sell_fuel': [False],
    'buy_fuel_at': [10, 0, 999],
    'buy_fuel': [False],
    'sell_gate_at': [5000, 0, 99999],
    'sell_gate': [False],
    'buy_gate_at': [5000, 0, 99999],
    'buy_gate': [False],
    'sell_intel': [False],
    'sell_intel_at': [100, 0, 999],
    'buy_intel': [False],
    'buy_intel_at': [100, 0, 999],
    'sell_passage': [False],
    'sell_passage_at': [50, 0, 999],
    'buy_passage': [False],
    'buy_passage_at': [50, 0, 999],
}

class Treaty(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = self.__uuid__
    
    def merge(self, other):
        other = other.flip()
        k1 = ['sell_passage', 'sell_passage_at', 'sell_intel', 'sell_intel_at', 'sell_gate', 'sell_gate_at', 'sell_fuel', 'sell_fuel_at', 'sell_li', 'sell_li_at', 'sell_si', 'sell_si_at', 'sell_ti', 'sell_ti_at']
        k2 = ['buy_passage', 'buy_passage_at', 'buy_intel', 'buy_intel_at', 'buy_gate', 'buy_gate_at', 'buy_fuel', 'buy_fuel_at', 'buy_li', 'buy_li_at', 'buy_si', 'buy_si_at', 'buy_ti', 'buy_ti_at']
        treaty = Treaty()
        if self.relation == other.relation:
            treaty.relation = self.relation
        for key in k1:
            treaty.__dict__[key] = self.__dict__[key]
            #print(treaty.__dict__[key])
        for key in k2:
            treaty.__dict__[key] = other.__dict__[key]
            #print(treaty.__dict__[key])
        return (treaty, treaty.flip())

    def flip(self, me):
        k1 = ['relation', 'name', 'me', 'other_player', 'accepted_by', 'rejected_by', 'replaced_by', 'sell_passage', 'sell_passage_at', 'sell_intel', 'sell_intel_at', 'sell_gate', 'sell_gate_at', 'sell_fuel', 'sell_fuel_at', 'sell_li', 'sell_li_at', 'sell_si', 'sell_si_at', 'sell_ti', 'sell_ti_at']
        k2 = ['relation', 'name', 'me', 'other_player', 'accepted_by', 'rejected_by', 'replaced_by', 'buy_passage', 'buy_passage_at', 'buy_intel', 'buy_intel_at', 'buy_gate', 'buy_gate_at', 'buy_fuel', 'buy_fuel_at', 'buy_li', 'buy_li_at', 'buy_si', 'buy_si_at', 'buy_ti', 'buy_ti_at']
        t = Treaty()
        for i in range(len(k1)):
            key1 = k1[i]
            key2 = k2[i]
            t.__dict__[key2] = self.__dict__[key1]
            t.__dict__[key1] = self.__dict__[key2]
        #t.p1 = self.p2
        t.other_player = me
        t.relation = self.relation
        #self.__dict__ = t.__dict__
        return t
    
    """ Equality check """
    def __eq__(self, other):
        k1 = ['name', 'me', 'accepted_by', 'replaced_by', 'sell_passage', 'sell_passage_at', 'sell_intel', 'sell_intel_at', 'sell_gate', 'sell_gate_at', 'sell_fuel', 'sell_fuel_at', 'sell_li', 'sell_li_at', 'sell_si', 'sell_si_at', 'sell_ti', 'sell_ti_at']
        k2 = ['relation', 'other_player', 'rejected_by', 'replaced_by', 'buy_passage', 'buy_passage_at', 'buy_intel', 'buy_intel_at', 'buy_gate', 'buy_gate_at', 'buy_fuel', 'buy_fuel_at', 'buy_li', 'buy_li_at', 'buy_si', 'buy_si_at', 'buy_ti', 'buy_ti_at']
        a = [self.relation == other.relation]
        for i in range(len(k1)):
            key1 = k1[i]
            key2 = k2[i]
            a.append((self.__dict__[key1] == other.__dict__[key1] and self.__dict__[key2] == other.__dict__[key2]))# or (self.key1 == other.key2 and self.key2 = other.key1))
            #print(self.__dict__[key1], other.__dict__[key1], key1)
            #print(self.__dict__[key2], other.__dict__[key2], key2)
            #print(a)
        return all(a)

Treaty.set_defaults(Treaty, __defaults, no_reset=['p2', 'p1'])
