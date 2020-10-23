from .uiplayer import UiPlayer


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class RaceViewer(UiPlayer):
    """ Interact with UI """
    def _post(self, action, me):
        pass


RaceViewer.set_defaults(RaceViewer, __defaults, no_reset=[])
