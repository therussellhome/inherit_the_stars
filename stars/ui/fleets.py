from .playerui import PlayerUI
import sys

""" Default values (default, min, max)  """
__defaults = {
    'fleet_list': [],
    'other_ships': [],
    'fleet_index': (0, 0, sys.maxsize),
    'ships': [],
    'fleet_orders': [],
}


""" """
class Fleets(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        if action.startswith('select_'):
            self.fleet_index = action.split('_')[1]
        self.fleet_list.append(
                '<th></th>'
                + '<th><i title="Name of the Fleet">Name</i></th>'
                + '<th><i title="X Cordinate">X</i></th>'
                + '<th><i title="Y Cordinate">Y</i></th>'
                + '<th><i title="Z Cordinate">Z</i></th>'
                + '<th><i class="fa-free-code-camp" title="Fuel">Fuel</i></th>'
                + '<th><i title="KT of People in fleet"></i>People</th>'
                + '<th><i class="ti" title="Titanium">in </i></th>'
                + '<th><i class="li" title="Lithium">in </i></th>'
                + '<th><i class="si" title="Silicon">in </i></th>')
        for i in range(len(self.player().fleets)):
            fleet = self.player().fleets[i]
            self.fleet_list.append('<tr>'
                + '<td><i class="button fas fa-eye" title="Select Fleet" onclick="post(\'fleets\', \'?select_' + str(i) + '\')"></i></td>'
                + '<td>' + str(fleet.name) + '</td>'
                + '<td>' + str(fleet.location.x) + '</td>'
                + '<td>' + str(fleet.location.y) + '</td>'
                + '<td>' + str(fleet.location.z) + '</td>'
                + '<td>' + str(fleet.__cache__['fuel']) + '</td>'
                + '<td>' + str(fleet.__cache__['cargo'].people) + '</td>'
                + '<td>' + str(fleet.__cache__['cargo'].titanium) + '</td>'
                + '<td>' + str(fleet.__cache__['cargo'].lithium) + '</td>'
                + '<td>' + str(fleet.__cache__['cargo'].silicon) + '</td>' + '</tr>')
        """self.other_ships.append(
                '<th><i title="Name of the ship">Name</i></th>'
                + '<th><i title="X Cordinate">X</i></th>'
                + '<th><i title="Y Cordinate">Y</i></th>'
                + '<th><i title="Z Cordinate">Z</i></th>'
                + '<th><i class="fa-free-code-camp" title="Fuel">Fuel</i></th>'
                + '<th><i title="KT of People in fleet"></i>People</th>'
                + '<th><i class="ti" title="Titanium">in </i></th>'
                + '<th><i class="li" title="Lithium">in </i></th>'
                + '<th><i class="si" title="Silicon">in </i></th>')
        for fleet in self.player().fleets:
            self.other_ships.append('<tr>'
                + '<td>' + ship.location.x + '</td>'
                + '<td>' + ship.location.y + '</td>'
                + '<td>' + ship.location.z + '</td>'
                + '<td>' + ship.get_fuel()[0] + '</td>'
                + '<td>' + ship.get_cargo()[0].people + '</td>'
                + '<td>' + ship.get_cargo()[0].titanium + '</td>'
                + '<td>' + fleet.get_cargo()[0].lithium + '</td>'
                + '<td>' + fleet.get_cargo()[0].silicon + '</td>' + '</tr>')"""
        self.ships.append(
                '<th><i title="Name of Ship Design">Ship Design</i></th>'
                + '<th><i class="fa-free-code-camp" title="Fuel">Fuel</i></th>'
                + '<th><i title="KT of People in fleet"></i>People</th>'
                + '<th><i class="ti" title="Titanium">in </i></th>'
                + '<th><i class="li" title="Lithium">in </i></th>'
                + '<th><i class="si" title="Silicon">in </i></th>')
        if len(self.player().fleets) > 0:
            for ship in self.player().fleets[self.fleet_index].ships:
                self.ships.append('<tr>'
                    + '<td>' + str(ship.ID) + '</td>'
                    + '<td>' + str(ship.fuel) + '</td>'
                    + '<td>' + str(ship.cargo.people) + '</td>'
                    + '<td>' + str(ship.cargo.titanium) + '</td>'
                    + '<td>' + str(ship.cargo.lithium) + '</td>'
                    + '<td>' + str(ship.cargo.silicon) + '</td>' + '</tr>')
        self.fleet_orders.append('<th><i title="Edit">Edit</i></th>'
                + '<th><i title="Description of order">Description</i></th>'
                + '<th><i title="X Cordinate">X</i></th>'
                + '<th><i title="Y Cordinate">Y</i></th>'
                + '<th><i title="Z Cordinate">Z</i></th>')
        #for i in self.player().fleets:
        if len(self.player().fleets) > 0:
            for I in range(len(self.player().fleets[self.fleet_index].orders)):
                order = self.player().fleets[self.fleet_index].orders[I]
                shown = ''
                if 'description' in order.__dict__:
                    shown += str('<td>' + str(order.description) + '</td>')
                shown += str('<td>' + str(order.location.x) + '</td>'
                            + '<td>' + str(order.location.y) + '</td>'
                            + '<td>' + str(order.location.z) + '</td>')
                self.fleet_orders.append('<tr>'
                    + '<td><i class="button fas fa-edit" title="Select order" onclick="show_screen(\'orders\'), post(\'orders\', \'?order=' + str(I) + ';fleet_index=' + str(self.fleet_index) + ';screen=fleets;start\')"></td>'
                    + shown + '</tr>')
        


Fleets.set_defaults(Fleets, __defaults, sparse_json=False)
