import sys
from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'shipyard_existing_designs': [[]],
    'shipyard_hull': ['Scout'],
    'shipyard_general_slots': [0, 0, sys.maxsize],
    'shipyard_orbital_slots': [0, 0, sys.maxsize],
    'shipyard_depot_slots': [0, 0, sys.maxsize],
    
}


""" """
class Shipyard(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        self.shipyard_existing_designs = self.player.existing_designs[0]
        self.shipyard_hull = self.pylayer.hulls[0]
        self.shipyard_general_slots = max(0, self.shipyard_general_slots)
        self.shipyard_orbital_slots = max(0, self.shipyard_orbital_slots)
        self.shipyard_depot_slots = max(0, self.shipyard_depot_slots)
    def shipyard_bombs(self):
        pass
    def shipyard_cloaks_and_ecm(self):
        pass
    def shipyard_defense(self):
        pass
    def shipyard_depot(self):
        pass
    def shipyard_engines(self):
        pass
    def shipyard_mech(self):
        pass
    def shipyard_scanners(self):
        pass
    def shipyard_orbital(self):
        pass
    def shipyard_weapons(self):
        pass

Shipyard.set_defaults(Shipyard, __defaults)
