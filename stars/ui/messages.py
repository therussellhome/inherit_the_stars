import sys
from .playerui import PlayerUI
from .. import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'messages_sender': '',
    'messages_date': '',
    'messages_text': '',
    'messages_index': (0, 0, sys.maxsize),
    'messages_number': '',
    'messages_keep': False,
    'messages_inbox': [],
}


""" Components of score are precomputed as part of turn generation """
class Messages(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        
        # Loads the file of messages
        dictionary = game_engine.load('Message', 'Inherit the Stars!')
        display = -1
        for i, msg in reversed(enumerate(self.player().messages)):
            if i > display and not msg.read:
                display = i
            # Gives the parameters to the message text
            if msg.msg_key in dictionary:
                text = dictionary[msg.msg_key]
            text = text.format(*msg.parameters)
            # Sets up the inbox
            # Adds the '...' if needed
            d = ''
            if len(text) > 58:
                d = '...'
            # TODO sender icon
            m = ''
            if not msg.read:
                m = ' font-weight:bold;'
            self.messages_inbox.append('<td>' + msg.date + '</td><td style="color: mediumslateblue; text-decoration: underline;' + m + " onclick="post(\'messages\', \'?id=' + str(i) + '\')">' + text[0:min(55, len(text))] + d + '</td>')
            if display == -1:
                display = len(msg) -1

        # Makes the previous and next arrows work
        if action.startswith('prev') and self.messages_index > 0:
            self.messages_index -= 1 
        if action.startswith('next') and self.messages_index < len(self.player().messages) - 1:
            self.messages_index += 1
        # Makes it open the clicked message 
        if action.startswith('id='):
            self.messages_index = int(action[3:])
        
        # Makes the keep checkbox work
        message = self.player().messages[self.messages_index]
        for msg in self.player().messages:
            if msg == message:
                msg.read = True
        if action.startswith('keep'):
            if not message.keep:
                message.keep = True
            elif message.keep:
                message.keep = False

        # Sets the message text, number, sender, date and whether to keep it
        if message.msg_key in dictionary:
            self.messages_text = dictionary[message.msg_key]
        self.messages_number = str(self.messages_index + 1) + ' of ' + str(len(self.player().messages))
        self.messages_sender = message.sender
        self.messages_date = message.date
        self.messages_keep = message.keep
        

Messages.set_defaults(Messages, __defaults, sparse_json=False)
