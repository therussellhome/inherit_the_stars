from .defaults import Defaults, apply_defaults
from .reference import Reference
from .tech import Tech



""" Default values (default, min, max)  """
__defaults = {
    'hull': Reference('Tech'),
    'category': 'Ship Design',
    'description': '',
    'components': {}, # map of tech names to count of components
    'race': Reference('Race'),
}


""" Ship design from which ships are built """
class ShipDesign(Tech):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Set the hull """
    def set_hull(self, tech):
        self.hull = Reference(tech)
        self.compute_stats()

    """ Add a component """
    def add_component(self, tech):
        tech = Reference(tech)
        if tech in self.components:
            self.components[tech] += 1
        else:
            self.components[tech] = 1
        self.compute_stats()

    """ Remove a component """
    def remove_component(self, tech):
        tech = Reference(tech)
        if tech in self.components:
            if self.components[tech] == 1:
                del self.components[tech]
            else:
                self.components[tech] -= 1
        self.compute_stats()

    """ Recompute self from components """
    def compute_stats(self):
        # Start by setting each field in the hull then add from the components
        for (k, v) in self.__dict__.items():
            # Skip certain fields and all strings
            if k in ['hull', 'components', 'race', '__cache__'] or isinstance(v, str):
                pass
            # Lists
            elif isinstance(v, list):
                self[k] = []
                self[k].extend(self.hull[k])
                for tech in self.components:
                    for i in range(0, self.components[tech]):
                        self[k].extend(tech[k])
            # If not a list assume it can be added
            else:
                self[k] = self.hull[k]
                for tech in self.components:
                    for i in range(0, self.components[tech]):
                        self[k] += tech[k]
    
    """ Recompute self from components """
    def max_armor(self):
        # Start by setting each field in the hull then add from the components
        armor = self.hull[armor]
        for tech in self.components:
            for i in range(0, self.components[tech]):
                armor += tech[armor]
    
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
        d = ShipDesign()
        d.set_hull(self.hull)
        for c in self.components:
            d.components[c] = self.components[c]
        d.compute_stats()
        return d


ShipDesign.set_defaults(ShipDesign, __defaults)
