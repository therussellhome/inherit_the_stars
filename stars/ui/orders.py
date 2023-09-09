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
    'fleet_id': '',
    'orders_id': '',
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
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        # Load values from existing order
        if action.startswith('load='):
            self.orders_id = action.split('=')[1]
            order = game_engine.get('Order/' + self.orders_id)
            for key in Order.defaults:
                if key == 'location':
                    if order.location.reference:
                        self.orders_destination = self.player.get_name(order.location.reference)
                        if order.location.reference != order.location.root_reference:
                            self.orders_destination += '<br/> at ' + self.player.get_name(order.location.root_reference)
                    else:
                        self.orders_destination = 'Deep Space'
                    self.orders_x = round(order.location.x, 2)
                    self.orders_y = round(order.location.y, 2)
                    self.orders_z = round(order.location.z, 2)
                else:
                    self['orders_' + key] = order[key]
        elif self.orders_id != '':
            order = game_engine.get('Order/' + self.orders_id)
        else:
            order = Reference('Order/')
        if self.fleet_id != '':
            fleet = game_engine.get('Fleet/' + self.fleet_id)
        else:
            fleet = Reference('Fleet/')
        # Display options
        for other_player in self.player.get_intel(by_type='Player'):
            if other_player != self.player:
                self.options_orders_transfer_to.append(other_player.ID)
        # Range check inputs
        self.orders_x = min(self.player.game.x, max(self.player.game.x * -1.0, self.orders_x))
        self.orders_y = min(self.player.game.y, max(self.player.game.y * -1.0, self.orders_y))
        self.orders_z = min(self.player.game.z, max(self.player.game.z * -1.0, self.orders_z))
        self.orders_ti_display = self.orders_load_ti * fleet.stats.cargo_max
        self.orders_li_display = self.orders_load_li * fleet.stats.cargo_max
        self.orders_si_display = self.orders_load_si * fleet.stats.cargo_max
        self.orders_pop_display = self.orders_load_pop * fleet.stats.cargo_max
        self.orders_fuel_display = self.orders_buy_fuel * fleet.stats.fuel_max
        # Load settings from orders library
        if self.orders_library != self.options_orders_library[0]:
            pass #TODO
        # Store updates back to the order
        for key in Order.defaults:
            if key == 'location':
                if self.orders_x != round(order.location.x, 2) \
                        or self.orders_y != round(order.location.y, 2) \
                        or self.orders_z != round(order.location.z, 2):
                    self.orders_destination = 'Deep Space'
                    order.location = Location(self.orders_x, self.orders_y, self.orders_z)
            else:
                order[key] = self['orders_' + key]
        # Topbar
        self.topbar.append('<i class="button far fa-times-circle"')
        if self.order_last_screen != '':
            self.topbar[-1] += ' title="Return to ' + str(self.order_last_screen) + ' screen" onclick="show_screen(\'' + str(self.order_last_screen) + '\')'
            if self.order_last_screen == 'fleets':
                self.topbar[-1] += ', post(\'fleets\', \'?select_' + str(self.fleet_id) + '\')'
            self.topbar[-1] += '">Back</i>'
        else:
            self.topbar[-1] += ' title="Close Orders screen" onclick="show_screen(null)">Close</i>'


for key in Order.defaults:
    __defaults['orders_' + key] = Order.defaults[key]

Orders.set_defaults(Orders, __defaults, sparse_json=False)
