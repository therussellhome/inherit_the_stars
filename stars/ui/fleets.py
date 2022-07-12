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
    def __init__(self, actions, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        for action in actions.split(';'):
            if action.startswith('select_'):
                self.fleet_index = action.split('_')[1]
            if action.startswith('delete_order='):
                to_delete = int(action.split('=')[1])
                del self.player.fleets[self.fleet_index].orders[to_delete]
        self.fleet_list.append('<th></th>'
            + '<th><i title="Name of the Fleet">Name</i></th>'
            + '<th><i title="X Cordinate">X</i></th>'
            + '<th><i title="Y Cordinate">Y</i></th>'
            + '<th><i title="Z Cordinate">Z</i></th>'
            + '<th><i class="fa-free-code-camp" title="Fuel">Fuel</i></th>'
            + '<th><i title="KT of People in fleet"></i>People</th>'
            + '<th><i class="ti" title="Titanium">in </i></th>'
            + '<th><i class="li" title="Lithium">in </i></th>'
            + '<th><i class="si" title="Silicon">in </i></th>')
        for i in range(len(self.player.fleets)):
            fleet = self.player.fleets[i]
            fleet_name = fleet.ID
            if hasattr(fleet, 'name'):
                fleet_name = fleet.name
            #intel = self.player.get_intel(reference=fleet)
            fleet_location = getattr(fleet, 'location')
            self.fleet_list.append('<tr>'
                + '<td><i class="button fas fa-eye" title="Select Fleet" onclick="post(\'fleets\', \'?select_' + str(i) + '\')"></i></td>'
                + '<td>' + str(fleet_name) + '</td>'#intel.name) + '</td>'
                + '<td>' + str(round(fleet_location.x, 4)) + '</td>'
                + '<td>' + str(round(fleet_location.y, 4)) + '</td>'
                + '<td>' + str(round(fleet_location.z, 4)) + '</td>'
                + '<td>' + str(fleet.fuel) + '</td>'
                + '<td>' + str(fleet.cargo.people) + '</td>'
                + '<td>' + str(fleet.cargo.titanium) + '</td>'
                + '<td>' + str(fleet.cargo.lithium) + '</td>'
                + '<td>' + str(fleet.cargo.silicon) + '</td>' + '</tr>')
        self.ships.append('<th><i title="Name of Ship Design">Ship Design</i></th>'
            + '<th><i class="fa-free-code-camp" title="Fuel">Fuel</i></th>'
            + '<th><i title="KT of People in fleet"></i>People</th>'
            + '<th><i class="ti" title="Titanium">in </i></th>'
            + '<th><i class="li" title="Lithium">in </i></th>'
            + '<th><i class="si" title="Silicon">in </i></th>')
        if len(self.player.fleets) > 0:
            for ship in self.player.fleets[self.fleet_index].ships:
                intel = self.player.get_intel(reference=ship)
                self.ships.append('<tr>'
                    + '<td>' + str(ship.description) + '</td>'
                    + '<td>' + str(ship.fuel) + '</td>'
                    + '<td>' + str(ship.cargo.people) + '</td>'
                    + '<td>' + str(ship.cargo.titanium) + '</td>'
                    + '<td>' + str(ship.cargo.lithium) + '</td>'
                    + '<td>' + str(ship.cargo.silicon) + '</td>' + '</tr>')
        self.fleet_orders.append('<th><i title="Edit">Edit</i></th>'
            + '<th><i title="Description of order">Description</i></th>'
            + '<th><i title="X Cordinate">X</i></th>'
            + '<th><i title="Y Cordinate">Y</i></th>'
            + '<th><i title="Z Cordinate">Z</i></th>'
            + '<th><i class="button fas fa-plus-circle" title="create order" onclick="show_screen(\'orders\'), post(\'orders\', \'?fleet_index=' + str(self.fleet_index) + ';create_order;screen=fleets;start\')"></th>')
        #for i in self.player.fleets:
        if len(self.player.fleets) > 0:
            for I in range(len(self.player.fleets[self.fleet_index].orders)):
                order = self.player.fleets[self.fleet_index].orders[I]
                shown = ''
                if 'description' in order.__dict__:
                    shown += str('<td>' + str(order.description) + '</td>')
                shown += str('<td>' + str(order.location.x) + '</td>'
                            + '<td>' + str(order.location.y) + '</td>'
                            + '<td>' + str(order.location.z) + '</td>')
                self.fleet_orders.append('<tr>'
                    + '<td><i class="button fas fa-edit" title="Select order" onclick="show_screen(\'orders\'), post(\'orders\', \'?load=fleet;' + str(self.fleet_index) + ';' + str(I) + '\')"></td>'
                    + shown + '<td><i class="button far fa-trash-alt" title="Delete Order" onclick="post(\'fleets\', \'?select_' + str(self.fleet_index) + ';delete_order=' + str(I) + '\')"></i></td>'
                    + '</tr>')
        


Fleets.set_defaults(Fleets, __defaults, sparse_json=False)
