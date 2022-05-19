import sys
from . import binning
from . import stars_math
from .defaults import Defaults
from .reference import Reference
from .location import Location


# (player, xyz) = hyperdenial
__denials = {}


""" Reset the hyperdenials """
def reset():
    global __denials
    __denials = {}


""" Calculate the effect of the denials against each fleet """
def calc(fleets):
    global __denials
    # Add all fleets into bins if the fleet is planned to move
    bins = {}
    for fleet in fleets:
        if not fleet.is_stationary:
            b = binning.num(fleet.location)
            if b in bins:
                bins[b].append(fleet)
            else:
                bins[b] = [fleet]
    # Calc the hyperdenial effects
    for ((player, xyz), denial) in __denials.items():
        location = Location(*xyz)
        for (fleet, bin_num) in binning.search(bins, location, denial.radius):
            if player == None or not fleet.player.get_treaty(player).hyperdenial_transit():
                print('location:', location)
                print('fleet:', fleet)
                distance = fleet.location - location
                if distance < denial.radius:
                    fleet.in_hyperdenial(denial.effect(distance), player, blackhole=(player==None))


""" Add a hyperdenial zone """
def _add_denial(location, denial, player=None):
    global __denials
    key = (player, location.xyz)
    if key not in __denials:
        __denials[key] = denial
    else:
        __denials[key] += denial#stars_math.volume_add(__denials[key], denial)


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID', # ID defaulted to a UUID if not provided from the new game screen
    'radius': (0.0, 0.0, sys.maxsize),
}


""" Represent 'hyperdenial' """
class HyperDenial(Defaults):
    """ Addition operator """
    def __add__(self, other):
        return HyperDenial(radius=stars_math.volume_add(self.radius, other.radius))

    """ Calculate the effect """
    def effect(self, distance):
        if distance >= self.radius:
            return 0.0
        print('r:', self.radius, 'd:', distance, 'result:', stars_math.volume(self.radius / max(1, distance)) - 4.15)
        return max(0.0, stars_math.volume(self.radius / max(1, distance)) - 4.15)

    """ Activate the hyperdenial """
    def activate(self, player, location):
        if self.radius > 0.0:
            _add_denial(location, self, player)#.radius, player)

HyperDenial.set_defaults(HyperDenial, __defaults)
