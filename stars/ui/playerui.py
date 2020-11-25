from .. import game_engine
from ..defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    # Shared with other forms and used to identify player
    'player_token': [''],
}


""" Components of score are precomputed as part of turn generation """
class PlayerUI(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = game_engine.get('Player', self.player_token)


PlayerUI.set_defaults(PlayerUI, __defaults)
