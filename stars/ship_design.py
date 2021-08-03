import sys
from .cost import Cost
from .defaults import Defaults, get_default
from .reference import Reference
from .tech import Tech



""" Default values (default, min, max)  """
__defaults = {
    'hull': Reference('Tech'),
    'category': 'Ship Design',
    'description': '',
    'components': {}, # map of tech names to count of components
    'slots_general': 0,
}


""" Ship design from which ships are built """
class ShipDesign(Tech):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Set the hull """
    def set_hull(self, tech):
        self.hull = Reference(tech)

    """ Add a component """
    def add_component(self, tech):
        tech = Reference(tech)
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
        self.merge(self.hull)
        for (t,cnt) in self.components.items():
            for i in range(0, cnt):
                self.merge(t)
        self.level = miniaturize_level
        (self.mass, self.cost) = self._miniaturize()

    """ Get the miniatuarized value """
    def reminiaturize_cost(self, level):
        return self._miniaturize()[1]

    """ How much past the base is the miniaturization """
    def _miniaturize(self):
        mass = 0
        cost = Cost()
        for (t,cnt) in ({self.hull:1} | self.components).items():
            modifier = t.miniaturization(self.level)
            mass += t.mass * modifier
            cost += t.cost * modifier
        return (mass, cost)

    """ Check if design is valid """
    def is_valid(self, level=None, race=None):
        if self.slots_general < 0 or self.slots_depot < 0 or self.slots_orbital < 0:
            return False
        if not self.hull.is_available(level=level, race=race):
            return False
        for tech in self.components:
            if not tech.is_available(level=level, race=race):
                return False
        return True

    """ Clone the design """
    def clone_design(self):
        clone = ShipDesign()
        clone.set_hull(self.hull)
        for c in self.components:
            clone.components[c] = self.components[c]
        return clone


ShipDesign.set_defaults(ShipDesign, __defaults)
