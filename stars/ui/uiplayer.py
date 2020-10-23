from .. import game_engine
from ..defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    # Shared with other forms and used to identify player
    'player_token': [''],
}


""" Components of score are precomputed as part of turn generation """
class UiPlayer(Defaults):
    """ Interact with UI """
    def post(self, action):
        me = game_engine.get('Player/' + self.player_token)
        # Always reset to default
        print(self.__dict__)
        self.reset_to_default()
        print(self.__dict__)
        # Process for the given player
        if me != None:
            self._post(action, me)

    """ Method to subclasses to override """
    def _post(self, action, me):
        pass

UiPlayer.set_defaults(UiPlayer, __defaults, no_reset=['player_token'])
