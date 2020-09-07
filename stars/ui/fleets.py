from .player import Player


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Fleets(Player):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Fleets.set_defaults(Fleets, __defaults, no_reset=[])
