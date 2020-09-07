from .player import Player


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Shipyard(Player):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Shipyard.set_defaults(Shipyard, __defaults, no_reset=[])
