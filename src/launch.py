from . import game_engine
from .defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    'launch_game': ['No Game Loaded'],
    'launch_player': [''],
    'options_launch_player': [[]],
    'launch_player_status': ['']
}


""" Represent Open Game action """
class Launch(Defaults):
    """ Interact with UI """
    def post(self, **kwargs):
        self.launch_player_status = ''
        # Always refresh the list of players
        self.options_launch_player = []
        games = game_engine.get('Game/')
        if len(games) > 0:
            self.launch_game = games[0].name
            # Load the players
            for player in game[0].players:
                #TODO filter out AIs
                self.options_launch_player.append(player.name)
                if player.name == self.launch_player:
                    self.launch_player_status = ''
        self.options_launch_player = game_engine.load_list('games')
        # Load the selected game
        if 'submit' in kwargs:
            pass


Launch.set_defaults(Launch, __defaults)
