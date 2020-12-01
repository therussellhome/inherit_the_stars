import sys
from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'shipyard_ship': [[]],
    'shipyard_existing_designs': [[]],
    'shipyard_design': [[]],
    'shipyard_tech': [[]],
    'shipyard_hull': ['Scout'],
    'shipyard_general_slots': [0, 0, sys.maxsize],
    'shipyard_orbital_slots': [0, 0, sys.maxsize],
    'shipyard_depot_slots': [0, 0, sys.maxsize],
    'shipyard_tech_category': ['Weapons'],
}


""" """
class Shipyard(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            #print('I')
            return
        # Ship display
        e = ''
        for d in self.shipyard_existing_designs:
            s = '<option>' + d + '</option>'
            if d == self.shipyard_ship:
                s = '<option selected="true">' + d + '</option>' 
            e += s
        self.shipyard_ship.append('<tr><td style="text-align: center" colspan="2" class="hfill">Existing Designs <select id="shipyard_existing_designs" onchange="post(\'shipyard\')">' \
            + e + '</select></td></tr>')

        # Shipyard design
        self.shipyard_design.append('<tr><td class="hfill">Design Name <input id="shipyard_name" class="hfill" onchange="post(\'shipyard\')"/></td></tr>')
        hulls = []
        for t in self.player.tech: 
            if t.is_available(self.player.tech_level, self.player.race) and t.category in ['Hull', 'Starbase']:
                hulls.append(t)
        

        for t in self.player.tech:
            link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
#            self.shipyard_design.append('<td class="hfill"><div class="tech tech_template">' + t.name + '</div></td>' \
#                    + '<td><i class="button far fa-trash-alt" title="Add to ship" onclick="post(\'Shipyard\', \'?del=' + link + '\')"></i></td>')
        r = ''
        for h in hulls:
            s = '<option>' + h.name + '</option>'
            if h == self.shipyard_hull:
                s = '<option selected="true">' + h + '</option>'
            r += s
        self.shipyard_design.append('<tr><td style="text-align: center" colspan="2" class="hfill">Hull <select id="shipyard_hull" onchange="post(\'shipyard\')">' \
            + r + '</select></td></tr>')
        self.shipyard_design.append('<tr><td>General Slots: <input disabled="true" id="shipyard_general_slots"/></td></tr>')
        self.shipyard_design.append('<tr><td>Orbital Slots: <input disabled="true" id="shipyard_orbital_slots"/></td></tr>')
        self.shipyard_design.append('<tr><td>Depot Slots: <input disabled="true" id="shipyard_depot_slots"/></td></tr>')
        self.shipyard_general_slots = self.shipyard_hull.slots_general
        self.shipyard_orbital_slots = self.shipyard_hull.slots_orbital
        self.shipyard_depot_slots = self.shipyard_hull.slots_depot

        # Sort tech
        shipyard_tech = []
        shipyard_filter_other = []
        for t in self.player.tech:
            if t.get_display_category() == self.shipyard_tech_category and t.is_available(self.player.tech_level, self.player.race):
                if t.category in ['Hull', 'Starbase']:
                    pass
                else:
                    link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
                    row = '<td class="hfill"><div class="tech tech_template">' + t.name + '</div></td>' \
                        + '<td><i class="button fas fa-cart-plus" title="Add to ship" onclick="post(\'shipyard\', \'?add=' + link + '\')"></i></td>'
                    shipyard_tech.append(row)
        #shipyard_tech.sort(key = lambda x: x[0])

        r = ''
        sf = ['Weapons', 'Defense', 'Electronics', 'Engines', 'Mechanicals', 'Heavy Equipment', 'Other']
        for f in sf:
            s = '<option>' + f + '</option>'
            if f == self.shipyard_tech_category:
                s = '<option selected="true">' + f + '</option>'
            r += s
        self.shipyard_tech.append('<tr><td style="text-align: center" colspan="2" class="hfill">Category <select id="shipyard_tech_category" onchange="post(\'shipyard\')">' \
            + r + '</select></td></tr>')
        for t in shipyard_tech:
            self.shipyard_tech.append(t)


Shipyard.set_defaults(Shipyard, __defaults, sparse_json=False)
