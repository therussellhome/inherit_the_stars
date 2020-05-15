from . import game_engine
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
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Tech, defaults=__defaults)
