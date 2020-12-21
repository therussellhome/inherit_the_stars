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

        dictionary = game_engine.load('messages', 'Messages Format')
        for key in dictionary:
            if key.split(".")[1] == 'introduction':
                self.player.messages.append(dictionary[key])
            messages_sender = key.split(".")[0]
            self.messages_sender = '<td><img title="' + messages_sender + '" src="/' + messages_sender + '.png"/></td><td>' + messages_sender + '</td>'
        index = 0
        if action.startswith('prev') and index > 0:
            index -= 1
        if action.startswith('next') and index < len(self.player.messages):
            index += 1
        self.messages_text = self.player.messages[index]

Messages.set_defaults(Messages, __defaults, sparse_json=False)
