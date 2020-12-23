import sys
from .playerui import PlayerUI
from .. import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'host_game': [[]],
    'host_name': [''],
    'host_turn': [''],
    'host_ready': [True],
    'host_autogen': [False],
    'host_status': [[]],
    'host_blocking': [False],
}


""" """
class Host(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        # List of games
        self.host_game = []
        for f in sorted(game_engine.load_list('Game')):
            link = f.replace('\'', '\\\'').replace('\"', '\\\"')
            g = game_engine.load_inspect('Game', f)
            if g:
                self.host_game.append('<td class="hfill rows">' + g.name
                    + '</td><td class="rows">Turn ' + str(int(g.hundreth / 100))
                    + '</td><td class="rows"><i class="button fas fa-external-link-alt" onclick="post(\'host\', \'?host=' + link + '\')"></i></td>')            
        # Get the game
        game = None
        if action.startswith('host='):
            game_engine.unregister()
            self.host_autoget = False
            game = game_engine.load('Game', action[5:])
        elif self.host_name != '':
            game = game_engine.get('Game/' + self.host_name)
        self.host_blocking = False
        self.host_ready = False
        if game:
            self.host_name = game.name
            game.update_players()
            if action == 'generate':
                for i in range(0, 100):
                    game.generate_hundreth()
                game.save()
            self.host_turn = 'Turn ' + str(int(game.hundreth / 100))
            if len(game.players) > 0:
                self.host_ready = True
            for p in game.players:
                ready = 'Ready to generate'
                if not p.ready_to_generate:
                    ready = 'Not ready'
                    self.host_ready = False
                self.host_status.append('<td>' + p.name + '</td>' \
                    + '<td style="text-align: right">' + ready + '</td>')
        else:
            self.host_name = ''
            self.host_turn = ''


Host.set_defaults(Host, __defaults, sparse_json=False)
