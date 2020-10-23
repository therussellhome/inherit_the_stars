from .uiplayer import UiPlayer


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class EnergyMinister(UiPlayer):
    """ Interact with UI """
    def _post(self, action, me):
        pass


EnergyMinister.set_defaults(EnergyMinister, __defaults, no_reset=[])
