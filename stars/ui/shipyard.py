import sys
from .playerui import PlayerUI
from ..reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'shipyard_ship': [[]],
    'shipyard_existing_designs': [''],
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
            return
        
        e = ''
        for r in self.player.existing_designs:
            s = '<option>' + r + '</option>'
            if r == self.shipyard_existing_designs:
                s = '<option selected="true">' + r + '</option>'
            e += s
        self.shipyard_ship.append('<td style="text-align: center" colspan="2" >Existing Designs <select id="shipyard_existing_designs" onchange="post(\'shipyard\')">' \
            + e + '</select></td>')

        # Shipyard design
        self.shipyard_design.append('<td>Design Name <input id="shipyard_name" onchange="post(\'shipyard\')"/></td>')
        hulls = []
        for t in self.player.tech: 
            if t.is_available(self.player.tech_level, self.player.race) and t.category in ['Hull', 'Starbase']:
                hulls.append(t)
        r = ''
        for h in hulls:
            s = '<option>' + h.name + '</option>'
            if h == self.shipyard_hull:
                s = '<option selected="true">' + h + '</option>'
            r += s
        self.shipyard_design.append('<td style="text-align: center" colspan="2">Hull <select id="shipyard_hull" onchange="post(\'shipyard\')">' \
            + r + '</select></td>')
        depot = []
        orbital = []
        general = []
        for t in self.shipyard_tech:
            if t in self.shipyard_design:
                if t.category == 'Depot':
                    depot.append(t)
                elif t.category == 'Orbital':
                    orbital.append(t)
                else:
                    general.append(t)
        for h in hulls:
            if h.name == self.shipyard_hull:
                g = h.slots_general
                o = h.slots_orbital
                d = h.slots_depot
        self.shipyard_design.append('<td id="shipyard_general_slots">General Slots: '  + str(len(general)) + '/' + str(g) + '</td>')
        self.shipyard_design.append('<td id="shipyard_orbital_slots">Orbital Slots: ' + str(len(orbital)) + '/'  + str(o) + '</td>')
        self.shipyard_design.append('<td id="shipyard_depot_slots">Depot Slots: ' + str(len(depot)) + '/' + str(d) + '</td>')
        
        # Add to ship design
        if action.startswith('add='):
            tech_add = Reference('Tech', action[4:])
            self.shipyard_design.append(tech_add)
        # Remove from ship design
        if action.startswith('del='):
            for t in self.shipyard_design:
                if t.name == action[4:]:
                    self.shipyard_design.remove(t)
                    break

        # Shipyard Tech
        # Sort tech
        shipyard_tech = []
        shipyard_filter_other = []
        for t in self.player.tech:
            if t.get_display_category() == self.shipyard_tech_category and t.is_available(self.player.tech_level, self.player.race) and t.category not in ['Hull', 'Starbase'] and t.get_display_category() != 'Planetary':
                    link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
                    row = '<td ><div class="tech tech_template">' + t.name + '</div></td>' \
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
        self.shipyard_tech.append('<td style="text-align: center" colspan="2" >Category <select id="shipyard_tech_category" onchange="post(\'shipyard\')">' \
            + r + '</select></td>')
        for t in shipyard_tech:
            self.shipyard_tech.append(t)


Shipyard.set_defaults(Shipyard, __defaults, sparse_json=False)
