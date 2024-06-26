import sys
from .playerui import PlayerUI
from ..reference import Reference
from .. import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'drafts_preview_index': (-1, -1, sys.maxsize),
    'drafts_preview_sender': '',
    'drafts_preview_receiver': '',
    'drafts_preview_number': '0 of 0',
    'drafts_preview_date': '',
    'drafts_preview_text': '',
    'drafts_preview_cache': '',
    'drafts_preview': '',
    'drafts_index': (-2, -2, sys.maxsize),
    'drafts_receiver': '',
    'drafts_number': '0 of 0',
    'drafts_text': '',
    'drafts_send': '<i class="far fa-paper-plane" style="padding-right: 1em"></i>',
    'options_drafts_receiver': [],
    'drafts_draft_box': [],
    'drafts_outbox': [],
    'drafts_draft_box_cache': [],
    'drafts_outbox_cache': [],
    'drafts_new': True,
}

""" Writing new messages and sending them to the other players, or even yourself """
class Drafts(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        # Load drafts
        self.load_cache('draft_box')
        self.load_cache('outbox')
        self.drafts_date = self.player.date
        self.drafts_preview_date = self.player.date
        self.options_drafts_receiver = []
        for p in self.player.get_intel(by_type='Player'):
            self.options_drafts_receiver.append(-p)
        print('receivers:', self.options_drafts_receiver)
        print('index:', self.drafts_index)
        # Handle message traffic
        if action.startswith('compose'):
            self.create_new()
            self.load_cache('draft_box', new=True)
            print('create_new')
        elif action.startswith('reply='):
            old = self.player.messages[int(action.split('=')[1])]
            self.create_new(old)
            self.load_cache('draft_box', new=True)
        elif action.startswith('send'):
            self.player.send_message(self.drafts_preview_index)
            if self.drafts_index == self.drafts_preview_index:
                self.drafts_index = -2
            elif self.drafts_index > self.drafts_preview_index:
                self.drafts_index -= 1
            self.drafts_preview_cache = ''
            self.drafts_preview_index = -1
            self.drafts_send = '<i class="far fa-paper-plane" style="padding-right: 1em"></i>'
            self.drafts_preview_number = '0 of 0'
            self.drafts_preview_sender = ''
            self.drafts_preview_receiver = ''
            self.drafts_preview_text = ''
            self.load_cache('draft_box', True)
            self.load_cache('outbox', True)
        elif action.startswith('save'):
            self.save_msg()
            self.load_cache('draft_box', True)
        elif action.startswith('cancel='):
            self.player.save_draft(self.player.outbox.pop(int(action[7:])))
            self.load_cache('draft_box', True)
            self.load_cache('outbox', True)
        elif action.startswith('delete='):
            key = int(action[7:])
            print('key:', key)
            if key == -1 or self.drafts_draft_box_cache[key]['index'] == -1:
                self.drafts_index = -2
            else:
                self.player.draft_box.pop(key)
            self.load_cache('draft_box', True)
        if action.startswith('update') or action.startswith('who'):
            if len(self.drafts_draft_box_cache) == 0:
                self.create_new()
                self.load_cache('draft_box', new=True)
            self.update_cache()

        # Makes the previous and next arrows work
        elif action.startswith('previous'):
            self.drafts_index += 1 
        elif action.startswith('next'):
            self.drafts_index -= 1
        # Makes it open the clicked message 
        elif action.startswith('drafts_id='):
            self.drafts_index = int(action[10:])
        elif action.startswith('outbox_id='):
            self.drafts_preveiw_index = int(action[10:])
            self.drafts_preview_cache = 'outbox'
            self.drafts_send = '<i class="fas fa-ban" onclick="post(\'drafts\', \'?cancel=' + str(self.drafts_preview_index) + '\')"></i>'
        elif self.drafts_index == -2:
            self.drafts_text = ''
            self.drafts_receiver = ''
        if action.startswith('preview:'):
            self.drafts_preview_cache = 'draft_box'
            self.drafts_preview_index = action[8:]
            if self.drafts_preview_index == -1:
                self.drafts_index = len(self.drafts_draft_box_cache) - 1
                self.drafts_preview_index = self.drafts_index
            self.drafts_send = '<i class="fas fa-paper-plane" title="Send message" style="padding-right: 1em" onclick="post(\'drafts\', \'?send\')"></i>'
        self.display_mail('draft_box')
        self.display_mail('outbox')
        self.display_drafts()
        self.drafts_preview = '<i class="fas fa-eye" style="padding-right: 1em" onclick="post(\'drafts\', \'?save\'); post(\'drafts\', \'?preview:' + str(self.drafts_index) + '\')"></i>'
        print('index:', self.drafts_index)

    def update_cache(self):
        msg = self.drafts_draft_box_cache[self.drafts_index]
        msg['text'] = self.drafts_text
        if self.drafts_receiver != '':
            msg['receiver'] = self.drafts_receiver
        msg['short'] = msg['text']
        if len(msg['short']) > 58:
            msg['short'] = msg['short'][:55] + '...'
        self.player.draft_box_cache = self.drafts_draft_box_cache
                    
    def save_msg(self):
        if len(self.drafts_draft_box_cache) == 0:
            self.create_new()
            self.load_cache('draft_box', new=True)
            self.update_cache()
        if self.drafts_index == -1 or self.drafts_draft_box_cache[self.drafts_index]['index'] == -1:
            msg = self.drafts_draft_box_cache[self.drafts_index]
            self.player.current_draft.message = msg['text']
            self.player.current_draft.receiver = Reference('Player/' + msg['receiver'])
            self.player.save_draft(self.player.current_draft)
            self.drafts_index = len(self.player.draft_box) -1
        elif self.drafts_index >= 0:
            msg = self.drafts_draft_box_cache[self.drafts_index]
            msg['text'] = self.drafts_text
            for i, m in enumerate(self.player.draft_box):
                if msg['index'] == i:
                    m.message = msg['text']
                    m.receiver = Reference('Player/' + msg['receiver'])
        
    def load_cache(self, cache, force=False, new=False):
        # Use cached messages
        print(cache)
        if len(self.player[cache + '_cache']) == 0 or force:
            msgs = []
            for i, m in enumerate(self.player[cache]):
                msg = {'index': i, 'receiver': -m.receiver}
                msg['text'] = m.message
                msg['icon'] = m.parameters[0]['icon']
                msg['sender'] = m.parameters[0]['name']
                msg['short'] = msg['text']
                if len(msg['short']) > 58:
                    msg['short'] = msg['short'][:55] + '...'
                msgs.append(msg)
            self.player[cache + '_cache'] = msgs
            print('set cache:', msgs)
        else:
            msgs = self.player[cache + '_cache']
            print('got cache:', msgs)
        if new:
            m = self.player.current_draft
            msg = {'index': -1, 'receiver': -m.receiver}
            msg['text'] = m.message
            msg['icon'] = m.parameters[0]['icon']
            msg['sender'] = m.parameters[0]['name']
            msg['short'] = msg['text']
            if len(msg['short']) > 53:
                msg['short'] = 'NEW: ' + msg['short'][:50] + '...'
            else:
                msg['short'] = 'NEW: ' + msg['short']
            msgs.append(msg)
            self.player[cache + '_cache'] = msgs
            self.drafts_index = -1
            print('end state:', msgs)
        self['drafts_' + cache + '_cache'] = msgs

    def display_mail(self, cache):
        for i, m in enumerate(self['drafts_' + cache + '_cache']):
            box = cache
            if box == 'draft_box':
                box = 'drafts'
            current = ''
            unbold = ''
            #unbold = 'font-weight: normal;'
            if ((self.drafts_index == i or (self.drafts_index == -1 and m['index'] == -1)) and cache == 'draft_box') or (self.drafts_preview_index == i and self.drafts_preview_cache == 'outbox'):
                current = 'background: darkblue;'
            icon = '<i '
            if box == 'drafts':
                icon += 'class="fas fa-trash-alt" title="Delete" onclick="post(\'drafts\', \'?delete=' + str(i) + '\')"'
            else:
                icon += 'class="fas fa-ban" title="Cancel" onclick="post(\'drafts\', \'?cancel=' + str(i) + '\')"'
            icon += '></i>'
            self['drafts_' + cache].append('<td style="' + current + '">' + m['icon'] + '</td><td style="' + current + unbold + '" title="To: ' + m['receiver'] + '" onclick="post(\'drafts\', \'?' + box + '_id=' + str(i) + '\')">' + m['short'] + '</td><td style="' + current + '">' + icon + '</td>')

    def display_drafts(self):
        print('index:', self.drafts_index)
        #preview tab
        if self.drafts_preview_index != -2 and self.drafts_preview_cache != '':
            m = self['drafts_' + self.drafts_preview_cache + '_cache'][self.drafts_preview_index]
            self.drafts_preview_text = m['text']
            self.drafts_preview_number = str(len(self['drafts_' + self.drafts_preview_cache + '_cache']) - self.drafts_preview_index) + ' of ' + str(len(self['drafts_' + self.drafts_preview_cache + '_cache']))
            self.drafts_preview_sender = '<div>' + m['icon'] + ' ' + m['sender'] + '</div>'
            self.drafts_preview_receiver = '<div>' + m['receiver'] + '</div>'
            self.drafts_date = self.player.date
        #drafts tab
        if self.drafts_index >= 0 and len(self.drafts_draft_box_cache) >= 1:
            m = self.drafts_draft_box_cache[self.drafts_index]
            self.drafts_text = m['text']
            self.drafts_number = str(len(self.drafts_draft_box_cache) - self.drafts_index) + ' of ' + str(len(self.drafts_draft_box_cache))
            self.drafts_preview_sender = '<div>' + m['icon'] + ' ' + m['sender'] + '</div>'
            self.drafts_date = self.player.date
        elif self.drafts_index == -1 and len(self.drafts_draft_box_cache) >= 1:
            m = self.drafts_draft_box_cache[-1]
            self.drafts_text = m['text']
            self.drafts_number = str(len(self.drafts_draft_box_cache) + 1) + ' of ' + str(len(self.drafts_draft_box_cache) + 1)
            self.drafts_preview_sender = '<div>' + m['icon'] + ' ' + m['sender'] + '</div>'
            self.drafts_date = self.player.date

    def create_new(self, old=None):
        m = {
            'parameters': [{
                'icon': '<i style="color: ' + self.player.race.icon_color + '; padding-right: 0" class="' + self.player.race.icon_class + '"></i>',
                'name': self.player.ID,
                }],
            'sender': Reference(self.player),
            'action': '<div title="reply" onclick="show_screen(\'drafts\'); post(\'drafts\', \'?reply:\')"><i class="fas fa-reply"></i></div>',
        }
        if old:
            m['receiver'] = old.sender
            m['parameters'].append(old.parameters[0])
            m['message'] = '\n* * * * * * * * *\nOn ' + old.date + ' ' + -old.sender + ' said:\n' + old.message
        self.player.new_draft(**m)
        self.drafts_index = -1
        
        


Drafts.set_defaults(Drafts, __defaults, sparse_json=False)
