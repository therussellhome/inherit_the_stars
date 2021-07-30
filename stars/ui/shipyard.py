import sys
from .playerui import PlayerUI
from ..reference import Reference
from ..ship_design import ShipDesign
from ..tech import TECH_GROUPS


""" Default values (default, min, max)  """
__defaults = {
    'shipyard_existing_design': '',
    'options_shipyard_existing_design': [],
    'shipyard_ship_overview': [], # table with ship tech display
    'shipyard_combat_chart': {},
    'shipyard_sensor_chart': [],
    'shipyard_engine_chart': {},
    'shipyard_ship_guts': [],
    'shipyard_ID': '',
    'shipyard_hull': '',
    'options_shipyard_hull': [],
    'shipyard_design': [],
    'shipyard_slots_general': '0/0',
    'shipyard_slots_depot': '0/0',
    'shipyard_slots_orbital': '0/0',
    'shipyard_tech': [],
    'shipyard_tech_group': 'Weapons',
    'options_shipyard_tech_group': TECH_GROUPS,
}


""" """
class Shipyard(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        design = None
        if 'ship_designs' not in self.player().__cache__:
            self.player().__cache__['ship_designs'] = list(self.player().ship_designs)
        for existing_design in self.player().__cache__['ship_designs']:
            if existing_design.ID == self.shipyard_existing_design:
                design = existing_design
                break
        # Actions
        if action == 'new_design':
            design = ShipDesign()
            self.player().__cache__['ship_designs'].append(design)
            self.shipyard_existing_design = design.ID
            self.shipyard_ID = ''
            self.shipyard_hull = ''
        elif action == 'copy_design':
            design = design.clone_design()
            self.player().__cache__['ship_designs'].append(design)
            self.shipyard_existing_design = design.ID
            self.shipyard_ID = ''
        elif action == 'delete_design':
            if design in self.player().ship_designs:
                self.player().ship_designs.remove(design)
            self.player().__cache__['ship_designs'].remove(design)
            self.shipyard_ID = ''
            design = None
        # Load / create design
        if design == None:
            if len(self.player().__cache__['ship_designs']) == 0:
                self.player().__cache__['ship_designs'].append(ShipDesign())
            design = self.player().__cache__['ship_designs'][0]
        # Design id
        if self.shipyard_ID == '':
            self.shipyard_ID = design.ID
        else:
            design.ID = self.shipyard_ID
        # Build design list after any chance for the name to change
        self.options_shipyard_existing_design = []
        for existing_design in self.player().__cache__['ship_designs']:
            self.options_shipyard_existing_design.append(existing_design.ID)
        self.shipyard_existing_design = design.ID

        # Hull selection
        for t in self.player().tech: 
            if t.is_available(self.player().tech_level, self.player().race) and t.category.endswith('Hull'):
                self.options_shipyard_hull.append(t.ID)
        if self.shipyard_hull != '':
            design.set_hull('Tech/' + self.shipyard_hull)

        # Add to ship design
        if action.startswith('add='):
            tech = Reference('Tech/' + action[4:])
            design.add_component(tech)
        # Remove from ship design
        if action.startswith('del='):
            tech = Reference('Tech/' + action[4:])
            design.remove_component(tech)
        # Recompute stats
        design.update(self.player().tech_level)

        # Check validity of design
        # valid designs are stored in the player's ship_designs
        # invalid designs are stored in the __cache__ and, if not fixed, will be lost when the player file is closed
        if design.is_valid(self.player().tech_level, self.player().race):
            if design not in self.player().ship_designs:
                self.player().ship_designs.append(design)
        else:
            if design.is_valid():
                self.user_alerts.append(design.ID + ' exceedes the allowed component slots')
            else:
                self.user_alerts.append(design.ID + ' contains unbuildable technology')
            if design in self.player().ship_designs:
                self.player().ship_designs.remove(design)

        # Display stats
        self.shipyard_ship_overview = design.html_overview()
        self.shipyard_combat_chart = design.html_combat(True)
        self.shipyard_sensor_chart = design.html_sensor(True)
        self.shipyard_engine_chart = design.html_engine(True)
        self.shipyard_ship_guts = design.html_guts()

        # Ship components
        for t in design.components:
            link = t.ID.replace('\'', '\\\'').replace('\"', '\\\"')
            count = ''
            if design.components[t] > 1:
                count = '<div style="color: lightseagreen">x' + str(design.components[t]) + '</div>'
            self.shipyard_design.append('<td class="hfill"><div class="tech tech_template">' + t.ID + '</div></td>' \
                    + '<td style="text-align: right;">' + count + '<i class="button far fa-trash-alt" title="Add to ship" onclick="post(\'shipyard\', \'?del=' + link + '\')"></i></td>')

        # Slots
        self.shipyard_slots_general = str(design.hull.slots_general - design.slots_general) + '/' + str(design.hull.slots_general)
        if design.slots_general < 0:
            self.shipyard_slots_general = '<span style="color: red">' + self.shipyard_slots_general + '</span>'
        self.shipyard_slots_depot = str(design.hull.slots_depot - design.slots_depot) + '/' + str(design.hull.slots_depot)
        if design.slots_depot < 0:
            self.shipyard_slots_depot = '<span style="color: red">' + self.shipyard_slots_depot + '</span>'
        self.shipyard_slots_orbital = str(design.hull.slots_orbital - design.slots_orbital) + '/' + str(design.hull.slots_orbital)
        if design.slots_orbital < 0:
            self.shipyard_slots_orbital = '<span style="color: red">' + self.shipyard_slots_orbital + '</span>'
        # Sort tech
        shipyard_tech = []
        for t in self.player().tech:
            if t.tech_group() == self.shipyard_tech_group and t.is_available(level=self.player().tech_level, race=self.player().race):
                link = t.ID.replace('\'', '\\\'').replace('\"', '\\\"')
                row = '<td ><div class="tech tech_template">' + t.ID + '</div></td>' \
                    + '<td><i class="button fas fa-cart-plus" title="Add to ship" onclick="post(\'shipyard\', \'?add=' + link + '\')"></i></td>'
                shipyard_tech.append((t.level.total_levels(), row))
        shipyard_tech.sort(key = lambda x: x[0])
        for t in shipyard_tech:
            self.shipyard_tech.append(t[1])


Shipyard.set_defaults(Shipyard, __defaults, sparse_json=False)
