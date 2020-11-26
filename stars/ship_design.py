from .defaults import Defaults
from .reference import Reference
from .tech import Tech



""" Default values (default, min, max)  """
__defaults = {
    'hull': [Reference('Tech')],
    'components': [[]],
}



class ShipDesign(Tech):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    """ Add a component """
    def add_component(self, tech):
        self.components.append(Reference(tech))
        self.compute_stats()


    """ Recompute self from components """
    def compute_stats(self):
        # Start by setting each field in the hull then add from the components
        for name in self.hull.list_of_defaults():
            tmp = getattr(self, name)
            # Lists
            if isinstance(tmp, list):
                tmp = getattr(self.hull, name).copy()
                for c in self.components:
                    tmp.extend(getattr(c, name))
            # Add numbers
            elif not isinstance(tmp, str):
                tmp = getattr(self.hull, name)
                for c in self.components:
                    tmp += getattr(c, name)
            setattr(self, name, tmp)


ShipDesign.set_defaults(ShipDesign, __defaults)
