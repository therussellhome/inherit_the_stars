from .. import game_engine
from .ui import UI


""" Default values (default, min, max)  """
__defaults = {
    # Shared with other forms and used to identify player
    'player_token': '',
}


""" Get the player object for use by child classes """
class PlayerUI(UI):
    """ Initialize the cached player object """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.player_token == '':
            self.__cache__['player'] = None
        else:
            self.__cache__['player'] = game_engine.get('Player/' + self.player_token)


    """ Return the cached player object """
    def player(self):
        return self.__cache__['player']


PlayerUI.set_defaults(PlayerUI, __defaults, sparse_json=False)
