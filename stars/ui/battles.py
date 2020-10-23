from .uiplayer import UiPlayer


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Battles(UiPlayer):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Battles.set_defaults(Battles, __defaults, no_reset=[])
