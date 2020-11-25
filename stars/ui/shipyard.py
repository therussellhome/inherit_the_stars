import sys
from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'shipyard_existing_designs': [[]],
    'shipyard_hull': [''],
    'shipyard_general_slots': [0, 0, sys.maxsize],
    'shipyard_orbital_slots': [0, 0, sys.maxsize],
    'shipyard_depot_slots': [0, 0, sys.maxsize],
    
}


""" """
class Shipyard(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        self.shipyard_existing_designs = self.player.existing_designs[0]
        self.shipyard_hull = self.player.hulls[0]
        self.shipyard_general_slots = max(0, self.shipyard_general_slots)
        self.shipyard_orbital_slots = max(0, self.shipyard_orbital_slots)
        self.shipyard_depot_slots = max(0, self.shipyard_depot_slots)

Shipyard.set_defaults(Shipyard, __defaults)
