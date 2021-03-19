from .defaults import Defaults, apply_defaults
from .reference import Reference
from .tech import Tech



""" Default values (default, min, max)  """
__defaults = {
    'hull': Reference('Tech'),
    'category': 'Ship Design',
    'description': '',
    'components': {}, # map of tech names to count of components
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
        # Start by setting each field in the hull then add from the components
        for (k, v) in self.__dict__.items():
            # Skip certain fields and all strings
            if k in ['hull', 'components', 'player', '__cache__'] or isinstance(v, str):
                pass
            # Minaturization
            elif k in ['cost', 'mass']:
                self[k] = self.hull.miniaturize(tech_level, k)
                for tech in self.components:
                    self[k] += tech.miniaturize(tech_level, k)
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
        armor = self.hull['armor']
        for tech in self.components:
            armor += tech['armor']
        return armor
    
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
