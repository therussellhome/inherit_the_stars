from . import game_engine
from .defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    'launch_player': [''],
}


""" Represent Open Game action """
class Launch(Defaults):
    """ Interact with UI """
    def post(self, action, **kwargs):
        pass


Launch.set_defaults(Launch, __defaults)
