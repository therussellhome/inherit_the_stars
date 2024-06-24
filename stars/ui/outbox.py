import sys
from .playerui import PlayerUI
from ..reference import Reference
from ..message import Message
from .. import game_engine


""" Default values (default, min, max)  """
__defaults = {
    'drafts_preview_index': (-1, -1, sys.maxsize),
    'drafts_preview_sender': '',
    'drafts_preview_number': '',
    'drafts_preview_date': '',
    'drafts_preview_text': '',
    'drafts_preview_cache': '',
    'drafts_index': (-1, -1, sys.maxsize),
    'drafts_reciver': '',
    'drafts_number': '',
    'drafts_text': '',
    'drafts_reciver_options': [],
    'drafts_save_box': [],
    'drafts_outbox': [],
    'drafts_draft_box_cache': [],
    'drafts_outbox_cache': [],
}


""" Components of score are precomputed as part of turn generation """
class Drafts(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return

        # Load drafts
        self.load_cache('draft_box')
        self.load_cache('outbox')
        self.drafts_date, self.drafts_preview_date = self.player.date
        self.drafts_reciver_options = []
        for p in self.player.get_intel(by_type='Player'):
            self.drafts_reciver_options.append(p.name)
            print('p.name')
        # Handle message traffic
        if action.startswith('compose'):
            self.create_new()
            print('create_new')
        elif action.startswith('reply='):
            old = self.player.messages[action.split('=')[1]]
            self.create_new(old)
        elif action.startswith('send'):
            self.player.send_message(self.drafts_index)
        elif action.startswith('save'):
            self.player.save_draft(self.drafts_draft_box_cache[self.draft_box_index])
        elif action.startswith('cancel='):
            self.player.save_draft(self.player.outbox.pop(action[7:]))
        elif action.startswith('delete='):
            self.player.drafts.pop(action[7:])
        if action.statswith('update'):
            self.drafts_draft_box_cache[self.drafts_index]['text'] = self.drafts_text
        if action.startswith('who'):
            m = self.drafts_draft_box_cache[self.drafts_index]
            m['reciver'] = self.drafts_reciver

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
        elif self.drafts_index == -1:
            for m in reversed(self.drafts_draft_box_cache):
                self.drafts_index = m['index']
                break
            else:
                self.drafts_index = len(self.drafts_draft_box_cache) - 1
        self.drafts_index = min(max(self.drafts_index, 0), len(self.drafts_draft_box_cache) - 1)
        elif action.startswinth('preview'):
            self.drafts_preview_cache, self.drafts_preview_index = action[7:].split(':')
        self.display_mail('safe_box')
        self.display_mail('outbox')
        self.display_drafts()
        
    def load_cache(self, cache, force=False, new=False):
        # Use cached messages
        if len(self.player[cache + '_cache']) == 0 or force:
            use_cache = cache
            if new:
                use_cache = cache + '_cache'
            msgs = []
            for i, m in enumerate(self.player[use_cache]):
                msg = {'index': i, 'date': m.date, 'reciver': m.reciver, 'action': ''}
                    msg['text'] = m.message
                    msg['icon'] = m.parameters[0]['icon']
                    msg['sender'] = m.parameters[0]['name']
                msg['short'] = msg['text']
                if len(msg['short']) > 58:
                    msg['short'] = msg['short'][:55] + '...'
                msgs.append(msg)
            self.player[cache + '_cache'] = msgs
        else:
            msgs = self.player[cache + '_cache']
        self['drafts_' + cache + '_cache'] = msgs

    def display_mail(self, cache):
        for m, i in enumerate(self['drafts_' + cache + '_cache']):
            box = cache
            if box == 'safe_box':
                box = 'drafts'
            current = ''
            unbold = ''
            #unbold = 'font-weight: normal;'
            if self.drafts == m['index']:
                current = 'background: darkblue;'
            icon = '<i'
            if box == 'drafts':
                icon += 'class="fas fa-trash-alt" onclick="post(\'drafts\', \'?delete=' + i + '\')"'
            else:
                icon += 'class="fas fa-ban" onclick="post(\'drafts\', \'?cancel=' + i + '\')"'
            icon += '></i>'
            self['drafts_' + cache].append('<td style="' + current + '">' + m['icon'] + '</td><td style="' + current + unbold + '" onclick="post(\'drafts\', \'?' + box + 'id=' + str(m['index']) + '\')">' + m['short'] + '</td><td style="' + current + '">' + icon + '</td>')

    def display_drafts(self):
        #preview tab
        if self.drafts_preview_index != -1:
            m = self['drafts_' + self.drafts_preview_cache + '_cache'][self.drafts_preview_index]
            self.drafts_preview_text = m['text']
            self.drafts_preview_number = str(len(self['drafts_' + self.drafts_preview_cache + '_cache']) - self.drafts_preview_index) + ' of ' + str(len(self['drafts_' + self.drafts_preview_cache + '_cache']))
            self.drafts_preview_sender = '<div>' + m.perameters[0]['icon'] + ' ' + m.perameters[0]['name'] + '</div>'
            self.drafts_date = self.player.date
        #drafts tab
        if self.drafts_index != 1:
            m = self.drafts_draft_box_cache[self.drafts_index]
            self.drafts_text = m['text']
            self.drafts_number = str(len(self.drafts_draft_box_cache) - self.drafts_index) + ' of ' + str(len(self.drafts_draft_box_cache))
            self.drafts_preview_sender = '<div>' + m.perameters[0]['icon'] + ' ' + m.perameters[0]['name'] + '</div>'
            self.drafts_date = self.player.date

    def create_new(self, old=None):
        m = {
            'parameters': [{
                'icon': '<i style="color: ' + self.player.race.icon_color + '; padding-right: 0" class="' + self.player.race.icon_class + '"></i>',
                'name': self.player.ID,
                }],
            'sender': Reference(self.player),
            'action': '<div title="reply" onclick="post(\'drafts\', \'?reply:\')"><i class="fas fa-reply"></i></div>',
        }
        if old:
            m['reciver'] = old.sender
            m['parameters'][1] = old.parameters[0]
            m['message'] = '\n* * * * * * * * *\nOn ' + old.date + ' ' + old.sender_name + ' said:\n' + old.message
        self.player.new_draft(**m)
        self.drafts_index = len(self.player.drafts) -1
        
        


Drafts.set_defaults(Drafts, __defaults, sparse_json=False)
