from .uiplayer import UiPlayer


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class Plans(UiPlayer):
    """ Interact with UI """
    def _post(self, action, me):
        pass


Plans.set_defaults(Plans, __defaults, no_reset=[])
