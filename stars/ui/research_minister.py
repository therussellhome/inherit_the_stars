import sys
from .playerui import PlayerUI
from ..reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'research_level': [[]],
    'research_queue': [[]],
    'research_tech_category':['Weapons'],
    'research_default_field': [[]],
    'research_tech': [[]],
}


""" """
class ResearchMinister(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        # Add to research queue
        if action.startswith('add='):
            tech_add = Reference('Tech', action[4:])
            self.player.research_queue.append(tech_add)
        # Remove from research queue
        if action.startswith('del='):
            for t in self.player.research_queue:
                if t.name == action[4:]:
                    self.player.research_queue.remove(t)
                    break
        # Current tech levels
        self.research_level.append('<td>' + self.player.tech_level.to_html(True) + '</td>')
        # Research queue
        research_queue = []
        for t in self.player.research_queue:
            link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
            research_queue.append(t.name)
            self.research_queue.append('<td class="hfill"><div class="tech tech_template">' + link + '</div></td>' \
                    + '<td><i class="button far fa-trash-alt" title="Add to queue" onclick="post(\'research_minister\', \'?del=' + link + '\')"></i></td>')
        # Sort tech
        research_tech = []
        research_filter = {
            'Weapons': ['Bomb', 'Missile', 'Beam'],
            'Defense': ['Shield', 'Armor'], 
            'Electronics': ['Scanner', 'Cloak', 'ECM'],
            'Engines': ['Engine'], 
            'Hulls & Mechanicals': ['Hull', 'Mechanical'], 
            'Heavy Equipment': ['Orbital', 'Depot'], 
            'Planetary': ['Planetary'],
            'Other': []
        }
        research_filter_other = []
        for f in research_filter:
            research_filter_other.extend(research_filter[f])
        cat = self.research_tech_category
        for t in self.player.tech:
            if t.category in research_filter[cat] or (cat == 'Other' and t.category not in research_filter_other):
                cost = t.level.calc_cost(self.player.race, self.player.tech_level, self.player.research_partial)
                if cost > 0 and t.name not in research_queue: 
                    link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
                    row = '<td class="hfill"><div class="tech tech_template">' + link + '</div></td>' \
                        + '<td><i class="button fas fa-cart-plus" title="Add to queue" onclick="post(\'research_minister\', \'?add=' + link + '\')"></i></td>'
                    research_tech.append((cost, row))
        research_tech.sort(key = lambda x: x[0])
        self.research_tech.append('<tr><td style="text-align: center" colspan="2" class="hfill">Category <select id="research_tech_category" onchange="post(\'research_minister\')">' \
            + '<option>Weapons</option>' \
            + '<option>Defense</option>' \
            + '<option>Electronics</option>' \
            + '<option>Engines</option>' \
            + '<option>Hulls &amp; Mechanicals</option>' \
            + '<option>Heavy Equipment</option>' \
            + '<option>Planetary</option>' \
            + '<option>Other</option>' \
            + '</select></td></tr>')
        for t in research_tech:
            self.research_tech.append(t[1])

ResearchMinister.set_defaults(ResearchMinister, __defaults, sparse_json=False)
