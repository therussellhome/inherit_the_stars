from .uiplayer import UiPlayer


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class PlanetaryMinister(UiPlayer):
    """ Interact with UI """
    def _post(self, action, me):
        pass


PlanetaryMinister.set_defaults(PlanetaryMinister, __defaults, no_reset=[])
