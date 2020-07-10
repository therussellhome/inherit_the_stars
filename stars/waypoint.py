import sys
from . import game_engine
from .defaults import Defaults
from .location import Location
from .location import locationReference
from .reference import Reference
from .star_system import Star_System


""" Default values (default, min, max)  """
__defaults = {
    'actions': [[]],
    # 'pre_load', 'unload', 'sell', 'buy', 'piracy', ...'load',
    'location': [],
    'fly_to': [Location()],
    'speed': [1, 1, 10],
    'description': [''],
    'standoff': [''],
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
    
    def move_to(self, location):
        if self.stantoff == 'No Standoff':
            for planet in game_engine.get('Planet/'):
                if self.location is planet.location:
                    self.fly_to = planet.system.get_outer_system(location)
            for ship in game_engine.get('Planet/'):
                if 
        if self.standoff 
    def calc_intercept(self):
        
