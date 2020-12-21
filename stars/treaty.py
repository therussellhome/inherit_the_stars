from .defaults import Defaults
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'other_player': [Reference('Player')],
    'relation': ['neutral'],
    'status': ['proposed'],
    # -1 is used to indicate no sell/buy
    'buy_ti': [-100, -100, 4000],
    'sell_ti': [-100, -100, 4000],
    'buy_si': [-100, -100, 4000],
    'sell_si': [-100, -100, 4000],
    'buy_li': [-100, -100, 4000],
    'sell_li': [-100, -100, 4000],
    'buy_fuel': [-1, -1, 50], #TODO Pam please balance this
    'sell_fuel': [-1, -1, 50], #TODO Pam please balance this
    'buy_gate': [-1000, -1000, 50000],
    'sell_gate': [-1000, -1000, 50000],
    'buy_hyper_denial': [-4000, -4000, 200000],
    'sell_hyper_denial': [-4000, -4000, 200000],
    'buy_intel': [-4000, -4000, 200000],
    'sell_intel': [-4000, -4000, 200000],
}


""" Treaty relationships """
TREATY_RELATIONSHIPS = ['enemy', 'neutral', 'team']

""" 
Treaty statuses 
active = accepted by both, actively in play
rejected = rejected by at least one party
proposed = proposed by me, awaiting other player's acceptance
pending = prosed by other player, awaiting my acceptance
signed = proposed by other player, accepted by me, awaiting finaliation by game engine
"""
TREATY_STATUS = ['active', 'rejected', 'proposed', 'pending', 'signed']


""" field list for merge/flip """
TREATY_BUY_SELL_FIELDS = ['buy_ti', 'sell_ti', 'buy_si', 'sell_si', 'buy_li', 'sell_li', 'buy_fuel', 'sell_fuel', 'buy_gate', 'sell_gate', 'buy_hyper_denial', 'sell_hyper_denial', 'buy_intel', 'sell_intel']


""" field list for merge/flip """
TREATY_HALF_FIELDS = ['_ti', '_si', '_li', '_fuel', '_gate', '_hyper_denial', '_intel']


""" The treaty class is from a given player's perspective to the other player """
class Treaty(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = self.__uuid__

    """ Both players proposed a treaty so copy each one's sell at into a combined treaty """
    # treaty status is not checked but should only be called with both treaties in the proposed state
    def merge(self, other):
        global TREATY_HALF_FIELDS
        self.status = 'pending'
        for f in TREATY_HALF_FIELDS:
            self['buy' + f] = other['sell' + f]

    """ Present to the other player contextualized/flipped for their reading """
    def for_other_player(self, me):
        global TREATY_HALF_FIELDS
        t = Treaty()
        t.other_player = Reference(me)
        if self.status == 'pending':
            t.status = 'proposed'
        elif self.status == 'proposed':
            t.status = 'pending'
        for f in TREATY_HALF_FIELDS:
            t['sell' + f] = self['buy' + f]
            t['buy' + f] = self['sell' + f]
        return t

    """ Is this an active treaty """
    def is_active(self):
        return (self.status in ['active', 'signed'])

    """ Is this a draft treaty """
    def is_draft(self):
        return (self.status in ['proposed', 'pending'])

    """ Is this a rejected treaty """
    def is_rejected(self):
        return (self.status == 'rejected')

Treaty.set_defaults(Treaty, __defaults)
