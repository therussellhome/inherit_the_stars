import sys
from .playerui import PlayerUI
from ..reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'research_level': [[]],
    'research_queue': [[]],
    'research_weapons': [[]],
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
            research_queue.append(t.name)
            # TODO handle tech with ' and " in its name
            self.research_queue.append('<td class="hfill"><div class="tech tech_template">' + t.name + '</div></td>' \
                    + '<td><i class="button far fa-trash-alt" title="Add to queue" onclick="post(\'research_minister\', \'?del=' + t.name + '\')"></i></td>')
        # Sort tech by cost
        research_tech = []
        for t in self.player.tech:
            cost = t.level.calc_cost(self.player.race, self.player.tech_level, self.player.research_partial)
            if cost > 0 and t.name not in research_queue:
                # TODO handle tech with ' and " in its name
                row = '<td class="hfill"><div class="tech tech_template">' + t.name + '</div></td>' \
                    + '<td><i class="button fas fa-cart-plus" title="Add to queue" onclick="post(\'research_minister\', \'?add=' + t.name + '\')"></i></td>'
                research_tech.append((cost, t.category, row))
        research_tech.sort(key = lambda x: x[0])
        # Sort components into categories
        for t in research_tech:
            if t[1] in ['Bomb', 'Missile', 'Beam']:
                self.research_weapons.append(t[2])

    def calc_cost(self, field):
        if field == 'energy':
            return round(research_modifier_energy * ((player.energy_tech_level ** 3) * 8 + 150))
        if field == 'weapons':
            return round(research_modifier_weapons * ((player.weapons_tech_level ** 3) * 8 + 150)) 
        if field == 'propulsion':
            return round(research_modifier_propulsion * ((player.propulsion_tech_level ** 3) * 8 + 150))
        if field == 'construction':
            return round(research_modifier_construction * ((player.construction_tech_level ** 3) * 8 + 150)) 
        if field == 'electronics':
            return round(research_modifier_electronics * ((player.electronics_tech_level ** 3) * 8 + 150))
        if field == 'biotechnology':
            return round(research_modifier_biotechnology * ((player.biotechnology_tech_level ** 3) * 8 + 150))
    def research_bombs(self):
        pass
    def research_cloaks_and_ecm(self):
        pass
    def research_defense(self):
        pass
    def research_depot(self):
        pass
    def research_engines(self):
        pass
    def research_hulls(self):
        pass
    def research_mech(self):
        pass 
    def research_orbital(self):
        pass
    def research_planetary(self):
        pass
    def research_scanners(self):
        pass
    def research_weapons(self):
        pass

ResearchMinister.set_defaults(ResearchMinister, __defaults)