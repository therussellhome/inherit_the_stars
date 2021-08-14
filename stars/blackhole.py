from .hyperdenial import HyperDenial
from .location import Location


""" Default values (default, min, max)  """
__defaults = {
    'location': Location(),
}


""" Represent a black hole """
class BlackHole(HyperDenial):
    """ Calculate the effect """
    def effect(self, distance):
        return super().effect(distance) * 100 #TODO game balance

    """ Add the black hole to the active hyperdenials """
    def activate(self):
        super().activate(Reference(''), self.location)

BlackHole.set_defaults(BlackHole, __defaults)
