import sys
import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'percent': [0, 0, 100],
    'kT': [0, 0, sys.maxsize]
}

""" Represent 'cloaking' """
class Scanner(game_engine.Defaults):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Cloak, defaults=__defaults)
