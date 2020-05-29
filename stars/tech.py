from .buildable import Buildable
from .tech_level import TechLevel


""" Default values (default, min, max)  """
__defaults = {
    'level': [TechLevel()],
    'race_requirements': ['']
}


""" Represent 'minerals' """
class Tech(Buildable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Determine if the item is available for a player's tech level """
    def is_available(self, player):
        if level.is_available(player.tech_level):
            # TODO check race requirements
            return True
        return False


Tech.set_defaults(Tech, __defaults)
