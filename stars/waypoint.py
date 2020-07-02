import sys
from . import game_engine
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'x': [0, -sys.maxsize, sys.maxsize],
    'y': [0, -sys.maxsize, sys.maxsize],
    'z': [0, -sys.maxsize, sys.maxsize],
    # (x, y, z; can be of an object, another ship)
    'actions': [[]],
    # actions=[''], .
    'speed': [1, 1, 10],
    'recipiants': [{}],
    # 'load':"your; Planet(), Fleet() or empty_space, salvage",
    # 'unload':"your; Planet(), Fleet() or salvege",
    # 'sell':"other; Planet()",
    # 'buy':"other; Planet()",
    #?'piracy':"other; Fleet()"?
    #?'pre_piracy':"other; Fleet()"?
    'transfers': [{}],
    # 'load':[[item, amount][item, amount][item, amount][item, amount][fuel, amount]],
    # 'unload':[[item, amount][item, amount][item, amount][item, amount][fuel, amount]],
    # 'sell':[[item, amount][item, amount][item, amount][fuel, amount]],
    # 'buy':[[item, amount][item, amount][item, amount][fuel, amount]],
    #?'piracy':[[item, amount][item, amount][item, amount][fuel, amount]]?
    #?'pre_piracy':[[item, amount][item, amount][item, amount][fuel, amount]]?
    
}


""" Class defining waypoints - edited by the player through fleet """
class Waypoint(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)
    
    
