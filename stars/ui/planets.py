from .player import Player


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Planets(Player):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Planets.set_defaults(Planets, __defaults, no_reset=[])
