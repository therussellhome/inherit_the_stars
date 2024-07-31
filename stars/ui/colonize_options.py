from .playerui import PlayerUI
import sys

""" Default values (default, min, max)  """
__defaults = {
    'colonize_options_min_ti_display': (0, -sys.maxsize, sys.maxsize),
    'colonize_options_min_li_display': (0, -sys.maxsize, sys.maxsize),
    'colonize_options_min_si_display': (0, -sys.maxsize, sys.maxsize),
    'colonize_options_min_hab_display': (0, -sys.maxsize, sys.maxsize),
    'colonize_options_min_hab': (50, -100, 100),
    'colonize_options_min_ti': (0, 0, 100),
    'colonize_options_min_li': (0, 0, 100),
    'colonize_options_min_si': (0, 0, 100),
}

keys = ['min_hab', 'min_ti', 'min_li', 'min_si']

""" Colonizing Options Screen """
class ColonizeOptions(PlayerUI):
    def __init__(self, actions, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        if 'load' in actions or 'reset' in actions:
            self.load()
        for key in keys:
            self['colonize_options_' + key + '_display'] = self['colonize_options_' + key]
        self.update()
                
    # Load values from existing order
    def load(self):
        for key in keys:
            self['colonize_options_' + key] = self.player['colonize_' + key]

    # Store updates back to the order
    def update(self):
        for key in keys:
            self.player['colonize_' + key] = self['colonize_options_' + key]



ColonizeOptions.set_defaults(ColonizeOptions, __defaults, sparse_json=False)
