import sys
from .cost import Cost
from .defaults import Defaults, get_default
from .reference import Reference
from .tech import Tech



""" Default values (default, min, max)  """
__defaults = {
    'category': 'Ship Design',
    'description': '',
    'components': {}, # map of tech names to count of components
    'slots_general': 0, # override the default of everything taking 1 general slot
}


""" Ship design from which ships are built """
class ShipDesign(Tech):
    """ Initialize defaults """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    """ Add a component """
    def add_component(self, tech, allow_hull_swap=True):
        tech = Reference(tech)
        # if a hull component then remove all other hull components
        if tech.is_hull() and allow_hull_swap:
            hull_swap = []
            for (t,cnt) in self.components.items():
                if t.is_hull():
                    hull_swap.append(t)
            for t in hull_swap:
                del self.components[t]
        if tech in self.components:
            self.components[tech] += 1
        else:
            self.components[tech] = 1

    """ Remove a component """
    def remove_component(self, tech, cnt=1):
        tech = Reference(tech)
        if tech in self.components:
            if self.components[tech] <= cnt:
                del self.components[tech]
            else:
                self.components[tech] -= cnt

    """ Recompute self from components """
    def update(self, miniaturize_level=None):
        if not miniaturize_level:
            miniaturize_level = self.level
        # Reset to default
        for key in Tech.defaults:
            if not isinstance(self[key], str):
                self[key] = get_default(self, key)
        for (t,cnt) in self.components.items():
            for i in range(0, cnt):
                self.merge(t)
        self.level = miniaturize_level
        (self.mass, self.cost) = self._miniaturize()

    """ How much past the base is the miniaturization """
    def _miniaturize(self):
        mass = 0
        cost = Cost()
        for (t,cnt) in self.components.items():
            modifier = t.miniaturization(self.level)
            mass += t.mass * modifier * cnt
            cost += t.cost * modifier * cnt
        return (mass, cost)

    """ Check if design is valid """
    def is_valid(self, level=None, race=None):
        hull_cnt = 0
        if self.slots_general < 0 or self.slots_depot < 0 or self.slots_orbital < 0:
            return False
        for (t,cnt) in self.components.items():
            if not t.is_available(level=level, race=race):
                return False
            if t.is_hull():
                hull_cnt += cnt
        if hull_cnt != 1:
            return False
        return True

    """ Get the hull of the ship """
    def hull(self):
        for tech in self.components:
            if tech.is_hull():
                return tech
        return Tech()

    """ This is a space station if it has orbital slots """
    def is_space_station(self):
        return self.hull().slots_orbital > 0

    """ Clone the design """
    def clone_design(self):
        clone = ShipDesign()
        clone.ID = str(self.ID) + '-copy'
        clone.description = str(self.description)
        for c in self.components:
            clone.add_component(c)
            clone.components[c] += self.components[c] -1
        return clone


ShipDesign.set_defaults(ShipDesign, __defaults)
