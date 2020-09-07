from .player import Player


""" Default values (default, min, max)  """
__defaults = {
}


""" """
class ResearchMinister(Player):
    """ Interact with UI """
    def _post(self, action, me):
        pass


ResearchMinister.set_defaults(ResearchMinister, __defaults, no_reset=[])
