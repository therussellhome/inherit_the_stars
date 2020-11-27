import sys
from .playerui import PlayerUI


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
        # Bound the msg index
        if self.messages_index == -1:
            self.messages_index = self.player.messages_unread
        self.messages_index = min(len(self.player.messages), self.messages_index)
        self.player.messages_unread = max(self.player.messages_unread, self.messages_index)
        self.messages_count = len(self.player.messages)
        self.messages_text = self.player.messages[self.messages_index]

Messages.set_defaults(Messages, __defaults, sparse_json=False)
