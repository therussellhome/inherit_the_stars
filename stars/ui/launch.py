from .. import game_engine
from ..defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    'launch_game': [''],
    'options_launch_game': [[]],
    'launch_player_status': [''],
    'launch_player_password': [''],
    # Shared with other forms and used to identify player
    'player_token': [''],
}


""" Represent Open Game action """
class Launch(Defaults):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if action == 'reset':
            self.reset_to_default()
        # Always refresh the list of games
        self.options_launch_game = game_engine.load_list('Player')
        self.options_launch_game.sort()
        # Load the selected game
        if action == 'go':
            game_engine.unregister()
            #TODO validate password
            p = game_engine.load('games', self.launch_game)
            # Fail if player not found
            self.player_token = str(id(p))
            

Launch.set_defaults(Launch, __defaults, sparse_json=False)
