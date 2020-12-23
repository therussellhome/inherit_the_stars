from .defaults import Defaults
from .reference import Reference
from .tech import Tech



""" Default values (default, min, max)  """
__defaults = {
    'hull': [Reference('Tech')],
    'category': ['Ship Design'],
    'description': [''],
    'components': [{}], # map of tech names to count of components
}



class ShipDesign(Tech):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = self.__uuid__.split('/')[1]

    """ Set the hull """
    def set_hull(self, tech):
        self.hull = Reference(tech)
        self.compute_stats()

    """ Add a component """
    def add_component(self, tech):
        if tech.name in self.components:
            self.components[tech.name] += 1
        else:
            self.components[tech.name] = 1
        self.compute_stats()

    """ Remove a component """
    def remove_component(self, tech):
        if tech.name in self.components:
            if self.components[tech.name] == 1:
                del self.components[tech.name]
            else:
                self.components[tech.name] -= 1
        self.compute_stats()

    """ Recompute self from components """
    def compute_stats(self):
        # Start by setting each field in the hull then add from the components
        for name in self.hull.list_of_defaults():
            tmp = getattr(self, name)
            # Lists
            if isinstance(tmp, list):
                tmp = getattr(self.hull, name).copy()
                for tech_name in self.components:
                    tech = Reference('Tech/' + tech_name)
                    for i in range(0, self.components[tech_name]):
                        tmp.extend(getattr(tech, name, []))
            # Add numbers
            elif not isinstance(tmp, str):
                tmp = getattr(self.hull, name)
                for tech_name in self.components:
                    tech = Reference('Tech/' + tech_name)
                    for i in range(0, self.components[tech_name]):
                        tmp += getattr(tech, name, 0)
            setattr(self, name, tmp)

    """ Check if design is valid """
    def is_valid(self, level=None, race=None):
        if self.slots_general < 0 or self.slots_depot < 0 or self.slots_orbital < 0:
            return False
        if not self.hull.is_available(level=level, race=race):
            return False
        for c in self.components:
            tech = Reference('Tech/' + c)
            if not tech.is_available(level=level, race=race):
                return False
        return True

    """ Clone the design """
    def clone_design(self):
        d = ShipDesign()
        d.set_hull(self.hull)
        for c in self.components:
            d.compoents[t] = self.components[t]
        d.compute_stats()
        return d

ShipDesign.set_defaults(ShipDesign, __defaults)
