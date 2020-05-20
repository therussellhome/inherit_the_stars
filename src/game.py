import sys
from . import game_engine
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'name': [''],
    'players': [[]],
    'date': [3000, 3000, sys.maxsize]
}


""" Class defining a game and everything in it """
class Game(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)


Game.set_defaults(Game, __defaults)
