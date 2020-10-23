from .uiplayer import UiPlayer


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Generate(UiPlayer):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Generate.set_defaults(Generate, __defaults, no_reset=[])
