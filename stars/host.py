from . import game_engine
from .defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    'host_game': [''],
    'options_host_game': [[]],
    'launch_player': [''],
    'options_launch_player': [[]],
    'host_autogen': [True],
    'host_player01': ['No Player'],
    'host_player01_status': [''],
    'host_player02': ['No Player'],
    'host_player02_status': [''],
    'host_player03': ['No Player'],
    'host_player03_status': [''],
    'host_player04': ['No Player'],
    'host_player04_status': [''],
    'host_player05': ['No Player'],
    'host_player05_status': [''],
    'host_player06': ['No Player'],
    'host_player06_status': [''],
    'host_player07': ['No Player'],
    'host_player07_status': [''],
    'host_player08': ['No Player'],
    'host_player08_status': [''],
    'host_player09': ['No Player'],
    'host_player09_status': [''],
    'host_player10': ['No Player'],
    'host_player10_status': [''],
    'host_player11': ['No Player'],
    'host_player11_status': [''],
    'host_player12': ['No Player'],
    'host_player12_status': [''],
    'host_player13': ['No Player'],
    'host_player13_status': [''],
    'host_player14': ['No Player'],
    'host_player14_status': [''],
    'host_player15': ['No Player'],
    'host_player15_status': [''],
    'host_player16': ['No Player'],
    'host_player16_status': ['']
}


""" Represent Open Game action """
class Host(Defaults):
    """ Interact with UI """
    def post(self, action):
        # Always refresh the list of games
        self.options_host_game = game_engine.load_list('games')
        # Load the selected game
        if action == 'submit':
            game_engine.unregister(None)
            game_engine.load(self.host_game)
        games = game_engine.get('Game/')
        if len(games) > 0:
            self.host_game = games[0].name
            # Load the players
            players = game[0].players
            for i in range(1, 17):
                key = 'host_player{:02d}'.format(i)
                if i <= len(players):
                    self.__dict__[key] = players[i - 1].name
                    self.__dict__[key + '_status'] = ''
                else:
                    self.__dict__[key] = 'No Player'
                    self.__dict__[key + '_status'] = ''
            

Host.set_defaults(Host, __defaults)
