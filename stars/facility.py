import sys
from .cost import Cost
from .tech import Tech
import copy


""" Default values (default, min, max)  """
__defaults = {
    'tech': [Tech()],
    'quantity': [0, 0, sys.maxsize],
}


""" Represent 'minerals' """
class Facility(Tech):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if self.tech.category == '' and len(args) > 0:
            self.tech.category = args[0]
    
    def build_prep(self):
        self.cost_incomplete = copy.copy(self.tech.cost)
    
    def colonize(self, player):
        if self.quantity == 0:
            self.tech = self.upgrade_available(player)
    
    def upgrade_available(self, player):
        best = self.tech
        for t in player.tech:
            if t.is_available(player.tech_level, player.race) and t.upgrade_path == best.upgrade_path and t.upgrade_level > best.upgrade_level:
                best = t
        if best == self.tech:
            return None
        return best
    
    def upgrade_cost(self, player, tech):
        scrap = self.tech.cost * self.quantity * (player.race.scrap_rate / 100)
        cost = tech.cost * self.quantity
        return cost - scrap
    
    def upgrade_complete(self, tech):
        self.tech = tech


Facility.set_defaults(Facility, __defaults)
