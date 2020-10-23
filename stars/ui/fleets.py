from .uiplayer import UiPlayer


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Fleets(UiPlayer):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Fleets.set_defaults(Fleets, __defaults, no_reset=[])
