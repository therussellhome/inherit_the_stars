from .defaults import Defaults
from .location import Location
from .reference import Reference
from .minerals import Minerals
import sys


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
    'minerals': Minerals(),
    'location': Location(),
    'ke': (0, 0, sys.maxsize),
    'target': Location(),
    'player': Reference('Player'),
    'decay_factor': (0.01, 0.0, 1.0),
}
#decay = mass * hyper**2 * decay_factor, mass -= decay"""


#what does it need to have?
#minerals is class
#location is class
#mass
#speed is hyper
#target is location
#player (only if TANSTAAFL) is reference
#decay rate

#from what does it inherit
#buildable
#not minerals (it has minerals)
