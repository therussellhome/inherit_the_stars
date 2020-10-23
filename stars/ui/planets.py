from .uiplayer import UiPlayer


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Planets(UiPlayer):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Planets.set_defaults(Planets, __defaults, no_reset=[])
