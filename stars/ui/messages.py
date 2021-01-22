import sys
from .playerui import PlayerUI
from .. import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'messages_sender': [''],
    'messages_date': [''],
    'messages_text': [''],
    'messages_index': [0, 0, sys.maxsize],
    'messages_number': [''],
    'messages_keep': [False],
    'messages_inbox': [[]],
}


""" Components of score are precomputed as part of turn generation """
class Messages(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        
        # Loads the file of messages
        dictionary = game_engine.load('Message', 'Inherit the Stars!') 
        for msg in self.player().messages:
            # Gives the parameters to the message text
            if msg.msg_key in dictionary:
                text = dictionary[msg.msg_key]
            text = text.format(*msg.parameters)
            # Sets up the inbox
            # TODO sender icon
            self.messages_inbox.append('<td style="color: mediumslateblue; text-decoration: underline;">' + msg.date + '</td>')
            # Adds the '...' if needed
            d = ''
            if len(text) > 63:
                d = '...'
            self.messages_inbox.append('<td style="color:mediumslateblue; text-decoration: underline;">' + text[0:min(61, len(text))] + d + '</td>')
        # Makes the previous and next arrows work
        if action.startswith('prev') and self.messages_index > 0:
            self.messages_index -= 1 
        if action.startswith('next') and self.messages_index < len(self.player().messages) - 1:
            self.messages_index += 1
        message = self.player().messages[self.messages_index]
        # Sets the message text, number, sender and date
        if message.msg_key in dictionary:
            self.messages_text = dictionary[message.msg_key]
        self.messages_number = str(self.messages_index + 1) + ' of ' + str(len(self.player().messages))
        self.messages_sender = message.sender
        self.messages_date = message.date
        

Messages.set_defaults(Messages, __defaults, sparse_json=False)
