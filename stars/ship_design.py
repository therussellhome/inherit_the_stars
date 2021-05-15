import sys
from .defaults import Defaults
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
    def compute_stats(self, tech_level):
        tech = [self.hull]
        for c in self.components:
            for i in range(0, self.components[c]):
                tech.append(c)
        self.init_from(tech, tech_level)
    
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
