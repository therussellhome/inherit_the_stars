from .playerui import PlayerUI
from .. import game_engine
from ..reference import Reference
from ..location import Location
from ..order import Order, standoff_options
import sys
import copy
from ..game import Game#finding Game.x through attribute trees

""" Default values (default, min, max)  """
__defaults = {
    'order_last_screen': 'null',
    'order_fleet_index': (-1, -1, sys.maxsize),
    'order_index': (-2, -2, sys.maxsize),
    'orders_close': [],
    'orders_get_sidebar': [],
    'orders_sidebar': [],
    'orders_xyz': [],
    'orders_info': '',
    'orders_set_edit': False,
    'orders_set_deep_space': True,
    'orders_destination': '',
    'options_orders_standoff': standoff_options,
    'orders_x': (0.0, -sys.maxsize, sys.maxsize),
    'orders_y': (0.0, -sys.maxsize, sys.maxsize),
    'orders_z': (0.0, -sys.maxsize, sys.maxsize),
    'orders_library': '--Load settings from orders library--',
    'options_orders_library': ['--Load settings from orders library--'],
    'options_orders_transfer_to': [''],
    'orders_ti_display': (0, -sys.maxsize, sys.maxsize),
    'orders_li_display': (0, -sys.maxsize, sys.maxsize),
    'orders_si_display': (0, -sys.maxsize, sys.maxsize),
    'orders_pop_display': (0, -sys.maxsize, sys.maxsize),
    'orders_fuel_display': (0, -sys.maxsize, sys.maxsize),
}


""" Order Screen """
class Orders(PlayerUI):
    def __init__(self, actions, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        for action in actions.split(';'):
            if action.startswith('load='):
                self.order_index = int(action.split('=')[1])
                self.orders_set_edit = False
            elif action == 'create_order':
                self.order_index = -1
                self.orders_set_edit = False
                fleet = self.get_fleet()
                fleet.orders.append(Order())
            elif action.startswith('fleet_index='):
                self.order_fleet_index = int(action.split('=')[1])
                self.orders_set_edit = False
            elif action.startswith('screen='):
                self.order_last_screen = action.split('=')[1]
            elif action == 'update':
                order = self.get_order()
                self.update(order)
            elif action.startswith('new'):
                self.orders_set_edit = True
                fleet = self.get_fleet()
                fleet.orders.insert(self.order_index, Order())
                self.orders_index += 1
                self.orders_set_deep_space = False
            elif action.startswith('edit'):
                self.orders_set_edit = True
                self.orders_set_deep_space = False
            elif action.startswith('waypoint='):
                if self.orders_set_edit:
                    order = self.get_order(('load' in actions))
                    order.location.reference = Reference(action.split('=')[1])
                    print(order.location.xyz, order.location.__dict__)
                    self.orders_x = order.location.xyz[0]
                    self.orders_y = order.location.xyz[1]
                    self.orders_z = order.location.xyz[2]
                self.orders_set_edit = False
                self.orders_set_deep_space = False
            elif action.startswith('set_deep_space'):
                self.orders_set_deep_space = True
        fleet = self.get_fleet()
        order = self.get_order(('load' in actions))
        # Display options
        for other_player in self.player.get_intel(by_type='Player'):
            if other_player != self.player:
                self.options_orders_transfer_to.append(other_player.ID)
        # Range check inputs
        self.orders_x = min(self.player.game.x, max(self.player.game.x * -1.0, self.orders_x))
        self.orders_y = min(self.player.game.y, max(self.player.game.y * -1.0, self.orders_y))
        self.orders_z = min(self.player.game.z, max(self.player.game.z * -1.0, self.orders_z))
        self.orders_ti_display = self.orders_ti * fleet.stats.cargo_max
        self.orders_li_display = self.orders_li * fleet.stats.cargo_max
        self.orders_si_display = self.orders_si * fleet.stats.cargo_max
        self.orders_pop_display = self.orders_pop * fleet.stats.cargo_max
        self.orders_fuel_display = self.orders_fuel * fleet.stats.fuel_max
        # Load settings from orders library
        if self.orders_library != self.options_orders_library[0]:
            pass #TODO
        # Topbar
        self.orders_close.append('<i class="button far fa-times-circle"')
        if self.order_last_screen != '':
            self.orders_close[-1] += ' title="Return to ' + str(self.order_last_screen) + ' screen" onclick="post(\'orders\', \'?update\'); show_screen(\'' + str(self.order_last_screen) + '\')'
            if self.order_last_screen == 'fleets':
                self.orders_close[-1] += '; post(\'fleets\', \'?select_' + str(self.order_fleet_index) + '\')'
            self.orders_close[-1] += '">Back</i>'
        else:
            self.orders_close[-1] += ' title="Close Orders screen" onclick="post(\'orders\', \'?update\'); show_screen(null)">Close</i>'
        """ Destination """
        disabled = ''
        if not self.orders_set_deep_space:
            disabled = ' disabled="true"'
        self.orders_xyz.append('<td><i class="button fas fa-edit" title="Set Deep Space" onclick="post(\'orders\', \'?set_deep_space\')"></i></td>')
        self.orders_xyz[-1] += \
                '<td style="text-align: left">X <input' + disabled + ' style="width: 15ex" id="orders_x" type="number" onchange="post(\'orders\')"/> ly</td>' +\
                '<td style="text-align: center">Y <input' + disabled + ' style="width: 15ex" id="orders_y" type="number" onchange="post(\'orders\')"/> ly</td>' +\
                '<td style="text-align: right">Z <input' + disabled + ' style="width: 15ex" id="orders_z" type="number" onchange="post(\'orders\')"/> ly</td>'
        """ Sidebar """
        # Close
        self.orders_sidebar.append('<td><i class="button fas fa-times-circle" title="Close" onclick="show_order_sidebar()"></i></td>')
        # Show Orders screen
        self.orders_sidebar.append('<td><img class="button" title="Orders" src="ships.png" onclick="show_screen(\'orders\')"/></td>')
        # Edit Button
        self.orders_sidebar.append('<td><i class="button fas fa-edit" title="Edit" onclick="post(\'orders\', \'?edit\'); show_screen(\'orders_info\')"></i></td>')
        # Add Waypoint
        self.orders_sidebar.append('<td><i class="button fas fa-plus-circle" title="Add Waypoint" onclick="post(\'orders\', \'?new\'); show_screen(\'orders_info\')"></i></td>')


    # load the selected fleet
    def get_fleet(self):
        if self.order_fleet_index != -1:
            fleet = self.player.fleets[self.order_fleet_index]
        else:
            fleet = Reference('Fleet/')
        return fleet
                
    # load the selected order from the fleet
    def get_order(self, load=False):
        fleet = self.get_fleet()
        if self.order_index != -2:
            order = fleet.orders[self.order_index]
            if load:
                self.load(order)
            else:
                self.update(order)
        else:
            order = Reference('Order/')
        return order

    # Load values from existing order
    def load(self, order):
        if order.location.reference:
            self.orders_set_deep_space = False
        for key in Order.defaults:
            if key == 'location':
                if order.location.reference:
                    self.orders_destination = self.player.get_name(order.location.reference)
                    if order.location.reference != order.location.root_reference:
                        self.orders_destination += '<br/> at ' + self.player.get_name(order.location.root_reference)
                else:
                    self.orders_destination = 'Deep Space'
                self.orders_x = order.location.x
                self.orders_y = order.location.y
                self.orders_z = order.location.z
            else:
                self['orders_' + key] = order[key]

    # Store updates back to the order
    def update(self, order):
        for key in Order.defaults:
            if key == 'location':
                if self.orders_x != round(order.location.x, 2) \
                        or self.orders_y != round(order.location.y, 2) \
                        or self.orders_z != round(order.location.z, 2):
                    self.orders_destination = 'Deep Space'
                    order.location = Location(self.orders_x, self.orders_y, self.orders_z)
            else:
                order[key] = self['orders_' + key]



for key in Order.defaults:
    __defaults['orders_' + key] = Order.defaults[key]

Orders.set_defaults(Orders, __defaults, sparse_json=False)
