from .uiplayer import UiPlayer


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Settings(UiPlayer):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Settings.set_defaults(Settings, __defaults, no_reset=[])
