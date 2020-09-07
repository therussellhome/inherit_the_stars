from .player import Player


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class EnergyMinister(Player):
    """ Interact with UI """
    def _post(self, action, me):
        pass


EnergyMinister.set_defaults(EnergyMinister, __defaults, no_reset=[])
