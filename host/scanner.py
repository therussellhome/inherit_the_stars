import sys
import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'anti_cloak': [0, 0, sys.maxsize],
    'penetrating': [0, 0, sys.maxsize],
    'range_for_100kt': [50, 0, sys.maxsize]
}

""" Represent 'scanner' """
class Scanner(game_engine.Defaults):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Scanner, defaults=__defaults)
