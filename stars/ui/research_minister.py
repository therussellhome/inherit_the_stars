from .playerui import PlayerUI
from ..reference import Reference
from ..tech import TECH_GROUPS
from ..tech_level import TECH_FIELDS


""" Default values (default, min, max)  """
__defaults = {
    'research_level': [[]],
    'research_queue': [[]],
    'research_default_field': [''],
    'options_research_default_field': [['<LOWEST>']],
    'research_tech_group':['Weapons'],
    'options_research_tech_group': [TECH_GROUPS],
    'research_tech': [[]],
}


# Build the default field list
for f in TECH_FIELDS:
    __defaults['options_research_default_field'][0].append(f.capitalize())


""" """
class ResearchMinister(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        # Default research field
        if self.research_default_field == '':
            self.research_default_field = self.player().research_field.capitalize()
        elif self.research_default_field != '<LOWEST>':
            self.player().research_field = self.research_default_field.lower()
        else:
            self.player().research_field = self.research_default_field
        # Add to research queue
        if action.startswith('add='):
            tech_add = Reference('Tech', action[4:])
            self.player().research_queue.append(tech_add)
        # Remove from research queue
        if action.startswith('del='):
            for t in self.player().research_queue:
                if t.name == action[4:]:
                    self.player().research_queue.remove(t)
                    break
        # Current tech levels
        self.research_level.append('<td>' + self.player().tech_level.to_html(True) + '</td>')
        # Research queue
        research_queue = []
        for t in self.player().research_queue:
            link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
            research_queue.append(t.name)
            self.research_queue.append('<td class="hfill"><div class="tech tech_template">' + t.name + '</div></td>'
                + '<td><i class="button far fa-trash-alt" title="Add to queue" onclick="post(\'research_minister\', \'?del=' + link + '\')"></i></td>')
        # Sort tech
        research_tech = []
        for t in self.player().tech:
            if t.tech_group() == self.research_tech_group and t.is_available(race=self.player().race) and t.name not in research_queue:
                cost = t.level.calc_cost(self.player().race, self.player().tech_level, self.player().research_partial)
                if cost > 0: 
                    link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
                    row = '<td class="hfill"><div class="tech tech_template">' + t.name + '</div></td>' \
                        + '<td><i class="button fas fa-cart-plus" title="Add to queue" onclick="post(\'research_minister\', \'?add=' + link + '\')"></i></td>'
                    research_tech.append((cost, row))
        research_tech.sort(key = lambda x: x[0])
        for t in research_tech:
            self.research_tech.append(t[1])

ResearchMinister.set_defaults(ResearchMinister, __defaults, sparse_json=False)
