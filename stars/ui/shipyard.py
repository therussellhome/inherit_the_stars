import sys
from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'shipyard_ship': [[]],
    'shipyard_design': [[]],
    'shipyard_tech': [[]],
    'shipyard_hull': ['Scout'],
    'shipyard_general_slots': [0, 0, sys.maxsize],
    'shipyard_orbital_slots': [0, 0, sys.maxsize],
    'shipyard_depot_slots': [0, 0, sys.maxsize],
    'shipyard_category': ['Weapons'],
}


""" """
class Shipyard(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        self.shipyard_existing_designs = self.player.existing_designs[0]
        self.shipyard_hull = self.player.hulls[0]
        self.shipyard_general_slots = max(0, self.shipyard_general_slots)
        self.shipyard_orbital_slots = max(0, self.shipyard_orbital_slots)
        self.shipyard_depot_slots = max(0, self.shipyard_depot_slots)

        # Ship components
        ship_components = []
        for t in self.player.ship_components:
            link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
            ship_components.append(t.name)
            self.ship_components.append('<td class="hfill"><div class="tech tech_template">' + t.name + '</div></td>' \
                    + '<td><i class="button far fa-trash-alt" title="Add to ship" onclick="post(\'Shipyard\', \'?del=' + link + '\')"></i></td>')
        # Sort tech
        shipyard_tech = []
        shipyard_filter_other = []
        for t in self.player.tech:
            if t.get_display_category() == shipyard_category and t.is_available(self.player.tech_level, self.player.race:
                link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
                row = '<td class="hfill"><div class="tech tech_template">' + t.name + '</div></td>' \
                    + '<td><i class="button fas fa-cart-plus" title="Add to queue" onclick="post(\'shipyard\', \'?add=' + link + '\')"></i></td>'
                shipyard_tech.append((cost, row))
        shipyard_tech.sort(key = lambda x: x[0])

        r = ''
        sf = ['Weapons', 'Defense', 'Electronics', 'Engines', 'Hulls & Mechanicals', 'Heavy Equipment', 'Planetary', 'Other']
        for f in shipyard_filter:
            s = '<option>' + f + '</option>'
            if f == cat:
                s = '<option selected="true">' + f + '</option>'
            r += s
        self.shipyard_tech.append('<tr><td style="text-align: center" colspan="2" class="hfill">Category <select id="shipyard_tech_category" onchange="post(\'shipyard\')">' \
            + r + '</select></td></tr>')
        for t in shipyard_tech:
            self.shipyard_tech.append(t[1])

        # Ship Design table
        ship_design.append('<tr><td class="hfill"><input id="shipyard_design_name" class="hfill" onchange="post(\'shipyard\')"/></td></tr>')
        hulls = []
        for t in self.player.tech:
            if t.is_available(player.tech_levels, player.race):
                if t.category in ['Hulls', 'Starbase']:
                    hulls.append(t)
                elif t.category not in ['Hulls', 'Starbase']:
                    shipyard_tech.append(t)
        r = ''
        for h in hulls:
            s = '<option>' + h + '</option>'
            if h == shipyard_hull:
                s = '<option selected="true">' + h + '</option>'
            r += s
        self.shipyard_design.append('<tr><td style="text-align: center" colspan="2" class="hfill">Hull <select id="shipyard_hull" onchange="post(\'shipyard\')">' \
            + r + '</select></td></tr>')

Shipyard.set_defaults(Shipyard, __defaults, sparse_json=False)
