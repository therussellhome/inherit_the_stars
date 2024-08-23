from .playerui import PlayerUI
import sys

""" Default values (default, min, max)  """
__defaults = {
    'settings_min_ti_display': (0, -sys.maxsize, sys.maxsize),
    'settings_min_li_display': (0, -sys.maxsize, sys.maxsize),
    'settings_min_si_display': (0, -sys.maxsize, sys.maxsize),
    'settings_min_hab_display': (0, -sys.maxsize, sys.maxsize),
    'settings_min_hab': (50, -100, 100),
    'settings_min_ti': (0, 0, 100),
    'settings_min_li': (0, 0, 100),
    'settings_min_si': (0, 0, 100),
}

keys = ['min_hab', 'min_ti', 'min_li', 'min_si']

""" """
class Settings(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        if 'load' in action or 'reset' in action:
            self.load()
        for key in keys:
            self['settings_' + key + '_display'] = self['settings_' + key]
        self.update()
                
    # Load values from existing order
    def load(self):
        for key in keys:
            self['settings_' + key] = self.player['colonize_' + key]

    # Store updates back to the order
    def update(self):
        for key in keys:
            self.player['colonize_' + key] = self['settings_' + key]




Settings.set_defaults(Settings, __defaults, sparse_json=False)
