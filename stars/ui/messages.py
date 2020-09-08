import sys
from .player import Player


""" Default values (default, min, max)  """
__defaults = {
    'messages_index': [-1, -1, sys.maxsize],
    'messages_count': [0, 0, sys.maxsize],
    'messages_text': [''],
}


""" Components of score are precomputed as part of turn generation """
class Messages(Player):
    """ Interact with UI """
    def _post(self, action, me):
        # Bound the msg index
        if self.messages_index == -1:
            self.messages_index = me.messages_unread
        self.messages_index = min(len(me.messages), self.messages_index)
        me.messages_unread = max(me.messages_unread, self.messages_index)
        self.messages_count = len(me.messages)
        self.messages_text = me.messages[self.messages_index]

Messages.set_defaults(Messages, __defaults, no_reset=['messages_index'])
