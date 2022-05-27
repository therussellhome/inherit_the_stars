from .playerui import PlayerUI
from .. import game_engine
from ..tech import TECH_GROUPS


""" Default values (default, min, max)  """
__defaults = {
    'tech_browser_tree': '',
    'options_tech_browser_tree': [],
    'tech_browser_group': TECH_GROUPS[0],
    'options_tech_browser_group': TECH_GROUPS,
    'tech_browser': [],
}


""" """
class TechBrowser(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        # List tech trees for loading
        self.options_tech_browser_tree = game_engine.load_list('Tech')
        if self.player:
            self.options_tech_browser_tree.insert(0, '«CURRENT PLAYER»')
            if self.tech_browser_tree not in self.options_tech_browser_tree:
                self.tech_browser_tree = '«CURRENT PLAYER»'
        elif self.tech_browser_tree not in self.options_tech_browser_tree:
            self.tech_browser_tree = 'Inherit the Stars!'
        if self.tech_browser_tree == '«CURRENT PLAYER»':
            tech_tree = self.player.tech
        else:
            tech_tree = game_engine.load('Tech', self.tech_browser_tree)
        # Sort tech
        tech = []
        for t in tech_tree:
            if t.tech_group() == self.tech_browser_group:
                tech.append((t.level.total_levels(), '<td><div class="tech tech_template">' + t.ID + '</div></td>'))
        tech.sort(key = lambda x: x[0])
        for t in tech:
            self.tech_browser.append(t[1])

TechBrowser.set_defaults(TechBrowser, __defaults, sparse_json=False)
