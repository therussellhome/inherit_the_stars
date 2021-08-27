from .hyperdenial import HyperDenial
from .location import Location


""" Default values (default, min, max)  """
__defaults = {
    'location': Location(),
}


""" Represent a black hole """
class BlackHole(HyperDenial):
    """ Add the black hole to the active hyperdenials """
    def activate(self):
        super().activate(None, self.location)

BlackHole.set_defaults(BlackHole, __defaults)
