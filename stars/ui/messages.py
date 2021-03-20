import sys
from .playerui import PlayerUI
from .. import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'messages_sender': '',
    'messages_date': '',
    'messages_text': '',
    'messages_index': (-1, -1, sys.maxsize),
    'messages_number': '',
    'messages_action': '',
    'messages_star': '',
    'messages_inbox': [],
}


""" Components of score are precomputed as part of turn generation """
class Messages(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return

        # Use cached messages
        if 'messages' not in self.player().__cache__:
            # Load message conversion files
            msg_text = game_engine.load('Message', 'Inherit the Stars!')
            if self.player().race.message_file != '':
                msg_text.update(game_engine.load('Message', self.player().race.message_file))
            msgs = []
            for i, m in enumerate(self.player().messages):
                msg = {'index': i, 'date': m.date, 'action': '', 'read': m.read}
                if m.sender ^ 'Player':
                    msg['link'] = 'show_screen(\'foreign_minister\')'
                    msg['text'] = m.message
                    #TODO
                else:
                    msg['icon'] = m.sender.get_icon()
                    msg['sender'] = m.sender.get_name()
                    msg['text'] = msg_text.get(m.sender.get_msg_key(m.message), m.message).format(*m.parameters)
                    msg['link'] = m.sender.get_link()
                    if m.action != '':
                        msg['action'] = '<i class="button fas fa-external-link-alt" title="Take Action" onclick="' + m.action + '"></i>'
                msg['short'] = msg['text']
                if len(msg['short']) > 58:
                    msg['short'] = msg['short'][:55] + '...'
                msgs.append(msg)
            self.player().__cache__['messages'] = msgs
        else:
            msgs = self.player().__cache__['messages']

        # Update star
        if action.startswith('star'):
            if self.player().messages[self.messages_index].star:
                self.player().messages[self.messages_index].star = False
            else:
                self.player().messages[self.messages_index].star = True

        # Makes the previous and next arrows work
        if action.startswith('prev'):
            self.messages_index += 1 
        elif action.startswith('next'):
            self.messages_index -= 1
        # Makes it open the clicked message 
        elif action.startswith('id='):
            self.messages_index = int(action[3:])
        elif self.messages_index == -1:
            for m in reversed(msgs):
                if not m['read']:
                    self.messages_index = m['index']
                    break
            else:
                self.messages_index = len(msgs) - 1
        self.messages_index = min(max(self.messages_index, 0), len(msgs) - 1)
        # Update read
        self.player().messages[self.messages_index].read = True
        msgs[self.messages_index]['read'] = True
        
        # Sets up the inbox
        newest_unread = len(msgs) - 1
        for m in reversed(msgs):
            unbold = ''
            if self.player().messages[m['index']].read:
                unbold = 'font-weight: normal;'
            current = ''
            if self.messages_index == m['index']:
                current = 'background: darkblue;'
            self.messages_inbox.append('<td style="' + current + '">' + m['icon'] + '</td><td style="' + current + unbold + '" onclick="post(\'messages\', \'?id=' + str(m['index']) + '\')">' + m['short'] + '</td><td style="' + current + unbold + '">' + m['date'] + '</td>')

        # Sets the message text, number, sender, date and whether to keep it
        m = msgs[self.messages_index]
        self.messages_text = m['text']
        self.messages_number = str(len(msgs) - self.messages_index) + ' of ' + str(len(msgs))
        self.messages_sender = '<div onclick="' + m['link'] + '">' + m['icon'] + ' ' + m['sender'] + '</div>'
        self.messages_date = m['date']
        self.messages_action = m['action']
        if self.player().messages[self.messages_index].star:
            self.messages_star = '<i class="fas fa-star"></i>'
        else:
            self.messages_star = '<i class="far fa-star"></i>'


Messages.set_defaults(Messages, __defaults, sparse_json=False)
