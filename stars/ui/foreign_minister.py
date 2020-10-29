from .player import Player


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class ForeignMinister(Player):
    """ Interact with UI """
    def _post(self, action, me):
        pass


ForeignMinister.set_defaults(ForeignMinister, __defaults, no_reset=[])
