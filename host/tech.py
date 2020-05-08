import game_engine
from cost import Cost
from tech_level import TechLevel


""" Default values (default, min, max)  """
__defaults = {
    'cost': [Cost()],
    'level': [TechLevel()],
    'race_requirements': ['']
}

""" Represent 'minerals' """
class Tech(game_engine.Defaults):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Tech, defaults=__defaults)
