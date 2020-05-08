from planet import Planet
import game_engine

""" Default values (default, min, max)  """
__defaults = {
    'distance': [0, 0, 0]
}

""" TODO """
class Sun(Planet):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Sun, defaults=__defaults)

""" TODO """
def _test():
    pass
