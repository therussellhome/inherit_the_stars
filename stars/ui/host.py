import sys
from .playerui import PlayerUI
from .. import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'host_game': [''],
    'options_host_game': [[]],
    'host_name': [''],
    'host_turn': [0, 0, sys.maxsize],
    'host_ready': [True],
    'host_autogen': [False],
    'host_status': [[]],
    'host_blocking': [False],
}


""" """
class Host(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        self.host_blocking = False
        self.options_host_game = game_engine.load_list('host')
        if self.host_game != '':
            self.host_ready = True
            game_engine.unregister()
            game = game_engine.load('host', self.host_game)
            game.update_players()
            if self.host_name != self.host_game:
                # First time showing this game so reset the host auto
                self.host_autogen = False
                self.host_name = self.host_game
                action = ''
            if action == 'generate':
                game.generate_turn()
                game.save()
            self.host_turn = game.turn
            if len(game.players) == 0:
                self.host_ready = False
            for p in game.players:
                ready = 'Ready to generate'
                if not p.ready_to_generate:
                    ready = 'Not ready'
                    self.host_ready = False
                self.host_status.append('<td>' + p.name + '</td>' \
                    + '<td style="text-align: right">' + ready + '</td>')
            game_engine.unregister()

Host.set_defaults(Host, __defaults)
