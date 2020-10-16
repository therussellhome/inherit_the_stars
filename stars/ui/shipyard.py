import sys
from .player import Player


""" Default values (default, min, max)  """
__defaults = {
    'shipyard_existing_designs': [''],
    'shipyard_hull': ['Scout'],
    'shipyard_general_slots': [0, 0, sys.maxsize],
    'shipyard_orbital_slots': [0, 0, sys.maxsize],
    'shipyard_depot_slots': [0, 0, sys.maxsize],
    
}


""" """
class Shipyard(Player):
    """ Interact with UI """
    def _post(self, action, me):
        pass
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

Shipyard.set_defaults(Shipyard, __defaults, no_reset=[])
