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
                self.fleet_index = int(action.split('_')[1])
            elif action.startswith('delete_order='):
                to_delete = int(action.split('=')[1])
                del self.player.fleets[self.fleet_index].orders[to_delete]
            elif action.startswith('ship='):
                ref = Reference('Ship/' + action.split('=')[1])
                for i in range(len(self.player.fleets)):
                    if ref in self.player.fleets[i].ships:
                        self.fleet_index = i
        self.fleet_list.append('<th></th>'
            + '<th><i class="no_pad_i" title="Name of the Fleet">Name</i></th>'
            + '<th><i class="no_pad_i" title="X Cordinate">X</i></th>'
            + '<th><i class="no_pad_i" title="Y Cordinate">Y</i></th>'
            + '<th><i class="no_pad_i" title="Z Cordinate">Z</i></th>'
            + '<th><i class="fa-free-code-camp no_pad_i" title="Fuel">Fuel</i></th>'
            + '<th><i class="no_pad_i" title="KT of People in fleet"></i>People</th>'
            + '<th><i class="ti no_pad_i" title="Titanium">in </i></th>'
            + '<th><i class="li no_pad_i" title="Lithium">in </i></th>'
            + '<th><i class="si no_pad_i" title="Silicon">in </i></th>')
        for i in range(len(self.player.fleets)):
            fleet = self.player.fleets[i]
            intel = self.player.get_intel(reference=fleet)
            if intel.name == fleet.ID:
                intel.name = 'Fleet #' + str(i+1)
            self.fleet_list.append('<tr>'
                + '<td><i class="button fas fa-eye" title="Select Fleet" onclick="post(\'fleets\', \'?select_' + str(i) + '\')"></i></td>'
                + '<td><i class="no_pad_i" title="' + str(intel.name) + '">' + '{:.8}'.format(intel.name) + '</i></td>'
                + '<td><i class="no_pad_i" title="' + str(intel.location[0]) + '">' + '{:.5}'.format(intel.location[0]) + '</i></td>'
                + '<td><i class="no_pad_i" title="' + str(intel.location[1]) + '">' + '{:.5}'.format(intel.location[1]) + '</i></td>'
                + '<td><i class="no_pad_i" title="' + str(intel.location[2]) + '">' + '{:.5}'.format(intel.location[2]) + '</i></td>'
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
            + '<th><i title="Speed of fleet">Speed</i></th>'
            + '<th><i title="X Cordinate">X</i></th>'
            + '<th><i title="Y Cordinate">Y</i></th>'
            + '<th><i title="Z Cordinate">Z</i></th>'
            + '<th><i class="button fas fa-plus-circle" title="create order" onclick="show_screen(\'orders\'), post(\'orders\', \'?create_order;fleet_index=' + str(self.fleet_index) + ';screen=fleets;start\')"></th>')
        #for i in self.player.fleets:
        if len(self.player.fleets) > 0:
            for I in range(len(self.player.fleets[self.fleet_index].orders)):
                order = self.player.fleets[self.fleet_index].orders[I]
                shown = ''
                if 'description' in order.__dict__:
                    shown += str('<td>' + str(order.description) + '</td>')
                else:
                    shown += str('<td></td>')
                labels = ['stargate', 'auto', 'stopped', 'alef', 'bet', 'gimel', 'dalet', 'he', 'waw', 'zayin', 'chet', 'tet', 'yod'];
                shown += str('<td>' + str(labels[order.speed]) + '</td>'
                            + '<td>' + str(order.location.x) + '</td>'
                            + '<td>' + str(order.location.y) + '</td>'
                            + '<td>' + str(order.location.z) + '</td>')
                self.fleet_orders.append('<tr>'
                    + '<td><i class="button fas fa-edit" title="Select order" onclick="show_screen(\'orders\'), post(\'orders\', \'?load=' + str(I) + ';fleet_index=' + str(self.fleet_index) + ';screen=fleets;start\'); show_order_sidebar()"></td>'
                    + shown + '<td><i class="button far fa-trash-alt" title="Delete Order" onclick="post(\'fleets\', \'?select_' + str(self.fleet_index) + ';delete_order=' + str(I) + '\')"></i></td>'
                    + '</tr>')
        


Fleets.set_defaults(Fleets, __defaults, sparse_json=False)
