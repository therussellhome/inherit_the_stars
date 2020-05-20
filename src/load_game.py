from . import game_engine
from .defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    'load_game_list': [''],
    'options_load_game_list': [[]],
    'load_game_auto': [True],
    'load_game_player01': ['No Player'],
    'load_game_player01_status': [''],
    'load_game_player02': ['No Player'],
    'load_game_player02_status': [''],
    'load_game_player03': ['No Player'],
    'load_game_player03_status': [''],
    'load_game_player04': ['No Player'],
    'load_game_player04_status': [''],
    'load_game_player05': ['No Player'],
    'load_game_player05_status': [''],
    'load_game_player06': ['No Player'],
    'load_game_player06_status': [''],
    'load_game_player07': ['No Player'],
    'load_game_player07_status': [''],
    'load_game_player08': ['No Player'],
    'load_game_player08_status': [''],
    'load_game_player09': ['No Player'],
    'load_game_player09_status': [''],
    'load_game_player10': ['No Player'],
    'load_game_player10_status': [''],
    'load_game_player11': ['No Player'],
    'load_game_player11_status': [''],
    'load_game_player12': ['No Player'],
    'load_game_player12_status': [''],
    'load_game_player13': ['No Player'],
    'load_game_player13_status': [''],
    'load_game_player14': ['No Player'],
    'load_game_player14_status': [''],
    'load_game_player15': ['No Player'],
    'load_game_player15_status': [''],
    'load_game_player16': ['No Player'],
    'load_game_player16_status': ['']
}


""" Represent Open Game action """
class LoadGame(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, **kwargs):
        # Always refresh the list of games
        self.options_load_game_list = game_engine.load_list('games')
        # Load the selected game
        if 'submit' in kwargs:
            game_engine.unregister(None)
            game_engine.load(self.load_game_list)
        games = game_engine.get('Game/')
        if len(games) > 0:
            self.load_game_list = games[0].name
            # Load the players
            players = game[0].players
            for i in range(1, 17):
                key = 'load_game_player{:02d}'.format(i)
                if i <= len(players):
                    self.__dict__[key] = players[i - 1].name
                    self.__dict__[key + '_status'] = ''
                else:
                    self.__dict__[key] = 'No Player'
                    self.__dict__[key + '_status'] = ''
            

LoadGame.set_defaults(LoadGame, __defaults)
