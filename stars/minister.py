from . import game_engine
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID',
    'name': '',
    'color': 'black',
}


""" The planetary minister controls the planetary construction phase of turn generation """
class Minister(Defaults):
    """ Initialize """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        game_engine.register(self)

    """ Get the icon """
    def get_icon(self, size='1em'):
        if self.ID == 'Admiralty':
            return '<img src="/admiralty.png" style="width: ' + size + '"/>'
        elif self.ID == 'Foreign':
            return '<img src="/foreign_minister.png" style="width: ' + size + '"/>'
        elif self.ID == 'Finance':
            return '<img src="/finance_minister.png" style="width: ' + size + '"/>'
        elif self.ID == 'Research':
            return '<img src="/research_minister.png" style="width: ' + size + '"/>'
        else:
            return '<img src="/planetary_minister.png" style="width: ' + size + '; background: ' + self.color + '"/>'

    """ Get the msg key """
    def get_msg_key(self, msg_key):
        if self.name == '':
            return self.ID.lower() + '.' + msg_key
        return 'planetary.' + msg_key

    """ Get the name """
    def get_name(self):
        if self.name == '':
            if self.ID == 'Admiralty':
                return self.ID
            return self.ID + ' Minister'
        return self.name + ' Minister'

    """ Get the link """
    def get_link(self):
        if self.ID == 'Admiralty':
            return 'show_screen(\'plans\')'
        elif self.ID == 'Foreign':
            return 'show_screen(\'foreign_minister\')'
        elif self.ID == 'Finance':
            return 'show_screen(\'finance_minister\')'
        elif self.ID == 'Research':
            return 'show_screen(\'research_minister\')'
        else:
            return 'show_minister(\'uuid=' + self.ID + '\')'


Minister.set_defaults(Minister, __defaults)
