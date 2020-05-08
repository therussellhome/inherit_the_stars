import sys
import game_engine

""" Default values (default, min, max)  """
__defaults = {
    'energy': [0, 0, sys.maxsize],
    'weapons': [0, 0, sys.maxsize],
    'propulsion': [0, 0, sys.maxsize],
    'construction': [0, 0, sys.maxsize],
    'electronics': [0, 0, sys.maxsize],
    'biotechnology': [0, 0, sys.maxsize]
}

""" Represent 'cost' """
class TechLevel(game_engine.Defaults):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(TechLevel, defaults=__defaults)
