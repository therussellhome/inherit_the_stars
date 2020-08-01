from . import game_engine
from .defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    'launch_game': [''],
    'options_launch_game': [[]],
    'launch_player': ['Host Mode'],
    'options_launch_player': [[]],
    'launch_autogen': [True],
    'launch_loaded_game': [''],
    'launch_player01': ['No Player'],
    'launch_player01_status': [''],
    'launch_player02': ['No Player'],
    'launch_player02_status': [''],
    'launch_player03': ['No Player'],
    'launch_player03_status': [''],
    'launch_player04': ['No Player'],
    'launch_player04_status': [''],
    'launch_player05': ['No Player'],
    'launch_player05_status': [''],
    'launch_player06': ['No Player'],
    'launch_player06_status': [''],
    'launch_player07': ['No Player'],
    'launch_player07_status': [''],
    'launch_player08': ['No Player'],
    'launch_player08_status': [''],
    'launch_player09': ['No Player'],
    'launch_player09_status': [''],
    'launch_player10': ['No Player'],
    'launch_player10_status': [''],
    'launch_player11': ['No Player'],
    'launch_player11_status': [''],
    'launch_player12': ['No Player'],
    'launch_player12_status': [''],
    'launch_player13': ['No Player'],
    'launch_player13_status': [''],
    'launch_player14': ['No Player'],
    'launch_player14_status': [''],
    'launch_player15': ['No Player'],
    'launch_player15_status': [''],
    'launch_player16': ['No Player'],
    'launch_player16_status': [''],
    'launch_loaded_autogen': ['Auto Generate: DISABLED'],
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
        self.options_launch_game = game_engine.load_list('games')
        self.launch_loaded_autogen = 'Auto Generate: DISABLED'
        # Get the currently loaded game
        games = game_engine.get('Game/')
        # Load info from the loaded game
        if len(games) > 0:
            self.launch_loaded_game = games[0].name
            if games[0].autogen_turn:
                self.launch_loaded_autogen = 'Auto Generate: ENABLED'
            if self.launch_game == '':
                self.launch_game = games[0].name
            if self.launch_game == games[0].name:
                self.options_launch_player = ['Host Mode']
                for player in games[0].players:
                    self.options_launch_player.append(player.name)
        # Load the player list
        elif self.launch_game != '':
            self.options_launch_player = game_engine.load_inspect('games', self.launch_game, 'Player/')
            self.options_launch_player.insert(0, 'Host Mode')
        else:
            self.options_launch_player = ['Host Mode']
        # Load the selected game
        if action == 'go':
            game_engine.unregister(None)
            game_engine.load('games', self.launch_game)
            games = game_engine.get('Game/')
            games[0].autogen_turn = self.launch_autogen
            self.launch_loaded_game = games[0].name
            if games[0].autogen_turn:
                self.launch_loaded_autogen = 'Auto Generate: ENABLED'
            else:
                self.launch_loaded_autogen = 'Auto Generate: DISABLED'
            if self.launch_player != 'Host Mode':
                for p in games[0].players:
                    if self.launch_player == p.name:
                        self.player_token = str(id(p))
        # Load the players
        for i in range(1, 17):
            key = 'launch_player{:02d}'.format(i)
            if len(games) > 0 and i <= len(games[0].players):
                self.__dict__[key] = games[0].players[i - 1].name
                self.__dict__[key + '_status'] = ''
            else:
                self.__dict__[key] = 'No Player'
                self.__dict__[key + '_status'] = ''
            

Launch.set_defaults(Launch, __defaults)
