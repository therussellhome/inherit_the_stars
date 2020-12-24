from .. import game_engine
from ..defaults import Defaults 


""" Default values (default, min, max)  """
__defaults = {
    'launch_game': [[]],
    'launch_player_password': [''],
    # Shared with other forms and used to identify player
    'player_token': [''],
}


""" Represent Open Game action """
class Launch(Defaults):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        self.launch_game = ['<th style="padding-right: 1em">Game</th><th style="text-align: left">Player</th><th colspan="2">Complete</th>']
        # Load the selected game
        if action.startswith('go='):
            game_engine.unregister()
            #TODO validate password
            p = game_engine.load('Player', action[3:])
            # Fail if player not found
            self.player_token = str(id(p))
            # Set the player object to autosave
            game_engine.set_auto_save(p)
        else:
            # List of games
            for f in sorted(game_engine.load_list('Player')):
                link = f.replace('\'', '\\\'').replace('\"', '\\\"')
                p = game_engine.load_inspect('Player', f)
                if p:
                    ready = 'No'
                    if p.ready_to_generate:
                        ready = '<i class="fas fa-check" style="color: green"></i>'
                    self.launch_game.append('<td class="rows" style="padding-right: 1em">' + p.game_name 
                        + '</td><td class="rows hfill">' + p.race.name 
                        + '</td><td class="rows">' + ready
                        + '</td><td class="rows" style="text-align: right"><i class="button fas fa-external-link-alt" onclick="post(\'launch\', \'?go=' + link + '\')"></i></td>')            
            

Launch.set_defaults(Launch, __defaults, sparse_json=False)
