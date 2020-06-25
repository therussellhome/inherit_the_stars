import sys
from . import game_engine
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'waypoints': [],
}


""" Class defining fleets - directly modifiable by the player """
class Fleet(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)
    
    def move(self):
        for ship in self.ships:
            ship.move(waypoints[0].speed)
    
    def execute(self, action):
        if action in waypoint.actions:
            for ship in self.ships:
                ship.waypoint = self.waypoints[0]
            

""" Ordered list of fleet preactions for use by the Game.generate_turn """
Fleet.preactions = [
    'pre_unload',
    'pre_load',
    'piracy',
]

""" Ordered list of fleet actions for use by the Game.generate_turn """
Fleet.actions = [
    'merge',
    'generate_fuel',
    'repair',
    'deploy_hyper_denial',
    'remote_mining',
    'lay_mines',
    'bomb',
    'colonize',
    'piracy',
    'sell',
    'unload',
    'scrap',
    'transfer',
    'buy',
    'load',
    'patrol',
    'route',
]
