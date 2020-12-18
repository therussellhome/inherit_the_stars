import sys
from .playerui import PlayerUI
from ..reference import Reference
from ..ship_design import ShipDesign


""" Default values (default, min, max)  """
__defaults = {
    'shipyard_existing_designs': [''],
    'options_shipyard_existing_designs': [[]],
    'shipyard_ship': [[]], # table with ship tech display
    'shipyard_name': [''],
    'shipyard_hull': [''],
    'options_shipyard_hull': [[]],
    'shipyard_design': [[]],
    'shipyard_tech': [[]],
    'options_shipyard_tech_category': [[]],
    'shipyard_tech_category': ['Weapons'],
}


""" """
class Shipyard(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        design = None
        for existing_design in self.player.ship_designs:
            if existing_design.name == self.shipyard_existing_designs:
                design = existing_design
        if design == None:
            design = ShipDesign()
            self.player.ship_designs.append(design)
            self.shipyard_name = design.name
        self.shipyard_ship = '<td><div class="tech tech_template">' + design.__uuid__ + '</div></td>'

        # Shipyard design
        for t in self.player.tech: 
            if t.is_available(self.player.tech_level, self.player.race) and t.category in ['Hull', 'Starbase']:
                self.options_shipyard_hull.append(t.name)
        
        # Show how many slots are used up
        design.set_hull('Tech/' + self.shipyard_hull)
        design.name = self.shipyard_name

        # Build design list after any chance for the name to change
        for existing_design in self.player.ship_designs:
            self.options_shipyard_existing_designs.append(existing_design.name)
        self.shipyard_existing_designs = design.name

        # Add to ship design
        if action.startswith('add='):
            design.add_component('Tech/' + action[4:])
        # Remove from ship design
        if action.startswith('del='):
            design.remove_component('Tech/' + action[4:])

        # Ship components
        for t in design.components:
            link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
            self.shipyard_design.append('<td class="hfill"><div class="tech tech_template">' + t.name + '</div></td>' \
                    + '<td><i class="button far fa-trash-alt" title="Add to ship" onclick="post(\'shipyard\', \'?del=' + link + '\')"></i></td>')

        self.shipyard_design.append('<td colspan="2"><table class="hfill"><tr>' \
                + '<td>General Slots:</td><td>' + str(design.hull.slots_general - design.slots_general) + '/' + str(design.hull.slots_general) + '</td>' \
                + '<td>Orbital Slots:</td><td>' + str(design.hull.slots_orbital - design.slots_orbital) + '/' + str(design.hull.slots_orbital) + '</td>' \
                + '<td>Depot Slots:</td><td>' + str(design.hull.slots_depot - design.slots_depot) + '/' + str(design.hull.slots_depot) + '</td>' \
                + '</tr></table></td>')

        # Shipyard tech
        # Sort tech
        shipyard_tech = []
        shipyard_filter_other = []
        for t in self.player.tech:
            if t.get_display_category() == self.shipyard_tech_category and t.is_available(self.player.tech_level, self.player.race) and t.category not in ['Hull', 'Starbase'] and t.get_display_category() != 'Planetary':
                    link = t.name.replace('\'', '\\\'').replace('\"', '\\\"')
                    row = '<td ><div class="tech tech_template">' + t.name + '</div></td>' \
                        + '<td><i class="button fas fa-cart-plus" title="Add to ship" onclick="post(\'shipyard\', \'?add=' + link + '\')"></i></td>'
                    shipyard_tech.append(row)
        # Tech category        
        categories = ['Weapons', 'Defense', 'Electronics', 'Engines', 'Mechanicals', 'Heavy Equipment', 'Other']
        for cat in categories:
            self.options_shipyard_tech_category.append(cat)
        self.shipyard_tech.append('<td style="text-align: center" colspan="2">Category <select id="shipyard_tech_category" onchange="post(\'shipyard\')"></select></td>')
        for t in shipyard_tech:
            self.shipyard_tech.append(t)

Shipyard.set_defaults(Shipyard, __defaults, sparse_json=False)
