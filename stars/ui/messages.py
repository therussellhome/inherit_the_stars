import sys
from .playerui import PlayerUI
from .. import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'messages_index': [-1, -1, sys.maxsize],
    'messages_count': [0, 0, sys.maxsize],
    'messages_text': [''],
}


""" Components of score are precomputed as part of turn generation """
class Messages(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return

        for key in game_engine.load('messages', 'Messages Format'):
            if key.split(".")[1] == 'introduction':
                self.player.messages.append(key)
            messages_sender = key.split(".")[0]
            self.messages_sender = '<td><img title="' + messages_sender + '" src="/' + messages_sender + '.png"/></td><td>' + messages_sender + '</td>'
        self.messages_text = self.player.messages[0]

Messages.set_defaults(Messages, __defaults, sparse_json=False)
