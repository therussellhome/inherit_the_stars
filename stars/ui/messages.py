import sys
from .playerui import PlayerUI
from .. import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'messages_text': [''],
    'messages_index': [0, 0, sys.maxsize],
    'messages_number': [''],
    'messages_keep': [False],
}


""" Components of score are precomputed as part of turn generation """
class Messages(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return

        dictionary = game_engine.load('messages', 'Messages Format')
        i = 0
        for key in dictionary:
            if key.split(".")[1] == 'introduction' and dictionary[key] not in self.player.messages:
                self.player.messages['3000.00:' + str(i)] = (dictionary[key])
                i += 1
        #print('length', len(self.player.messages))
        if action.startswith('prev') and self.messages_index > 0:
            self.messages_index -= 1
        if action.startswith('next') and self.messages_index < len(self.player.messages) - 1:
            self.messages_index += 1
        self.messages_text = self.player.messages[self.messages_index]
        self.messages_number = str(self.messages_index + 1) + ' of ' + str(len(self.player.messages))

Messages.set_defaults(Messages, __defaults, sparse_json=False)
