from .player import Player


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Settings(Player):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Settings.set_defaults(Settings, __defaults, no_reset=[])
