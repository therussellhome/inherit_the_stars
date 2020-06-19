import sys
from . import game_engine
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
}


""" Class defining fleets - directly modifiable by the player """
class Fleet(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)

""" Ordered list of fleet preactions for use by the Game.generate_turn """
Fleet.preactions = [
    'pre_load',
    'pre_unload',
]

""" Ordered list of fleet actions for use by the Game.generate_turn """
Fleet.actions = [
    'merge',
    'generate_fuel',
    'repair',
    'deploy_hyper_denial',
    'remote_mining',
    'trade',
    'load',
    'piracy',
    'lay_mines',
    'bomb',
    'colonize',
    'unload',
    'scrap',
    'transfer',
    'patrol',
    'route',
]
