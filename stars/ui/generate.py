from .player import Player


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Generate(Player):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Generate.set_defaults(Generate, __defaults, no_reset=[])
