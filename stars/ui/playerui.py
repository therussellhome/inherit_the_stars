from .. import game_engine
from .ui import UI


""" Default values (default, min, max)  """
__defaults = {
    # Shared with other forms and used to identify player
    'player_token': '',
}

""" Temporary values (default, min, max)  """
__tmp_defaults = {
    'player': None,
}


""" Get the player object for use by child classes """
class PlayerUI(UI):
    """ Initialize the cached player object """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.player_token != '':
            self.player = game_engine.get('Player/' + self.player_token)


PlayerUI.set_defaults(PlayerUI, __defaults, __tmp_defaults, sparse_json=False)
