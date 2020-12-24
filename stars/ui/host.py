import sys
from .ui import UI
from .. import game_engine


# Text for not ready
_not_ready = '<span style="color: red">Not Ready</span>'


""" Default values (default, min, max)  """
__defaults = {
    'host_game': [[]],
    'host_name': [''],
    'host_turn': [''],
    'host_ready': [_not_ready],
    'host_autogen': [False],
    'host_status': [[]],
    'host_blocking': [False],
}


""" """
class Host(UI):
    def __init__(self, action, **kwargs):
        global _not_ready
        super().__init__(**kwargs)
        # Get the game
        game = None
        if action.startswith('host='):
            game_engine.unregister()
            self.host_autogen = False
            game = game_engine.load('Game', action[5:])
        elif self.host_name != '':
            game = game_engine.get('Game/' + self.host_name)
        self.host_blocking = False
        self.host_ready = _not_ready
        if game:
            self.host_name = game.name
            game.update_players()
            if action == 'generate':
                game.new_turn()
            self.host_turn = 'Turn ' + str(int(game.hundreth / 100))
            if len(game.players) > 0:
                self.host_ready = 'Ready'
            for p in game.players:
                ready = 'Ready to generate'
                if not p.ready_to_generate:
                    ready = _not_ready
                    self.host_ready = _not_ready
                self.host_status.append('<td>' + p.name + '</td>' \
                    + '<td style="text-align: right">' + ready + '</td>')
        else:
            self.host_name = ''
            self.host_turn = ''
        # List of games
        self.host_game = []
        for f in sorted(game_engine.load_list('Game')):
            link = f.replace('\'', '\\\'').replace('\"', '\\\"')
            g = game_engine.load_inspect('Game', f)
            if g:
                self.host_game.append('<td class="hfill rows">' + g.name
                    + '</td><td class="rows">Turn ' + str(int(g.hundreth / 100))
                    + '</td><td class="rows"><i class="button fas fa-external-link-alt" onclick="post(\'host\', \'?host=' + link + '\')"></i></td>')


Host.set_defaults(Host, __defaults, sparse_json=False)
