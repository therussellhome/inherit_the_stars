import copy
import sys
from .defaults import Defaults
from .tech import Tech



""" Default values (default, min, max)  """
__defaults = {
    'hull': [Tech()],
    'components': [[]],
    'is_starbase': [False]
}



class ShipDesign(Tech):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    """ Add a component """
    def add_component(self, tech):
        self.components.append(copy.copy(tech))
        self.compute_stats()


    """ Recompute self from components """
    def compute_stats(self):
        # Reset stats
        hull = self.hull.__dict__
        # Start by resetting each field in the hull
        for name in hull:
            # Skip strings
            if not isinstance(hull[name], str):
                self.__dict__[name] = copy.copy(hull[name])
                # Extend lists
                if isinstance(hull[name], list):
                    for c in self.components:
                        self.__dict__[name].extend(getattr(c, name))
                # Add numbers
                else:
                    for c in self.components:
                        self.__dict__[name] += getattr(c, name)


ShipDesign.set_defaults(ShipDesign, __defaults)
