import sys
from .buildable import Buildable
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'tech': [Reference('Tech')],
    'quantity': [0, 0, sys.maxsize],
}


""" Represent 'minerals' """
class Facility(Buildable):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    """ Return the cost to build """
    def add_to_build_queue(self, race=None, upgrade_to=None):
        super().add_to_build_queue(race, upgrade_to)
        if upgrade_to:
            return (self.upgrade_to.cost - self.tech.scrap_value(race)) * self.quantity
        return self.tech.cost

    """ Add to facility count or finalize upgrade """
    def build_complete(self, race=None, upgrade_to=None):
        super().build_complete(race, upgrade_to)
        if upgrade_to:
            self.tech = Reference(upgrade_to)
        else:
            self.quantity += 1

    def colonize(self, player):
        if self.quantity == 0:
            upgrade = self.upgrade(player)
            if upgrade:
                self.tech = upgrade
    
    def upgrade(self, category, player):
        if self.under_construction:
            return None
        best = self.tech
        for t in player.tech:
            if t.is_available(player.tech_level) and t.upgrade_path == category and t.upgrade_level > best.upgrade_level:
                best = t
        if best == self.tech:
            return None
        return best

Facility.set_defaults(Facility, __defaults)
