import sys
from . import game_engine
from .defaults import Defaults
from .component import Component


""" Default values (default, min, max)  """
__defaults = {
    'general_slots': [],
    'depot_slots': [],
}

class ShipHull(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

ShipHull.set_defaults(ShipHull, __defaults)
