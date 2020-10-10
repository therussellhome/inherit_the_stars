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
    """ Interact with UI """
    def post(self, action):
        if action == 'reset':
            self.reset_to_default()
        # Always refresh the list of games
        self.options_launch_game = []
        for host in game_engine.load_list('host'):
            self.options_launch_game.append(host + ' ** HOST **')
        for player in game_engine.load_list('games'):
            self.options_launch_game.append(player)
        self.options_launch_game.sort()
        # Load the selected game
        if action == 'go':
            game_engine.unregister()
            if self.launch_game[-11:] == ' ** HOST **':
                #TODO validate password
                game_engine.load('host', self.launch_hame[:-11])
            else:
                #TODO validate password
                p = game_engine.load('games', self.launch_game)
                # Fail if player not found
                self.player_token = str(id(p))
            

Launch.set_defaults(Launch, __defaults)
