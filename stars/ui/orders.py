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
    'order_last_screen': 'fleets',
    'order_fleet_index': (-1, -1, sys.maxsize),
    'order_index': (-2, -2, sys.maxsize),
    'topbar': [],
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
            if action == 'create_order':
                self.order_index = -1
            if action.startswith('fleet_index='):
                self.order_fleet_index = int(action.split('=')[1])
            if action.startswith('screen='):
                self.order_last_screen = action.split('=')[1]
            if action == 'update':
                fleet = self.player.fleets[self.order_fleet_index]
                order = fleet.orders[self.order_index]
                self.update(order)
        if self.order_fleet_index != -1:
            fleet = self.player.fleets[self.order_fleet_index]
        else:
            fleet = Reference('Fleet/')
        if 'create_order' in actions:
            # Create a new order object
            fleet.orders.append(Order())
        if self.order_index != -2:
            order = fleet.orders[self.order_index]
            if 'load' in actions:
                self.load(order)
            else:
                self.update(order)
        else:
            order = Reference('Order/')
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
        self.topbar.append('<i class="button far fa-times-circle"')
        if self.order_last_screen != '':
            self.topbar[-1] += ' title="Return to ' + str(self.order_last_screen) + ' screen" onclick="post(\'orders\', \'?update\'), show_screen(\'' + str(self.order_last_screen) + '\')'
            if self.order_last_screen == 'fleets':
                self.topbar[-1] += ', post(\'fleets\', \'?select_' + str(self.order_fleet_index) + '\')'
            self.topbar[-1] += '">Back</i>'
        else:
            self.topbar[-1] += ' title="Close Orders screen" onclick="post(\'orders\', \'?update\'), show_screen(null)">Close</i>'
                
    # Load values from existing order
    def load(self, order):
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
