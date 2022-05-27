from .playerui import PlayerUI
from ..reference import Reference
from ..location import Location
from ..order import Order
import sys
import copy
from ..game import Game#finding Game.x through attribute trees

depart_options = [
    'immediately',
    'after x years',
    'repair to x',
    'remain indef',
]

standoff_options = [
    'No Standoff',
    'Avoid Detection',
    'Penetrating Minimum',
    'Anti-Cloak Minimum',
    'Hyper-Denial Minimum',
    ]

separate_display = [
    'speed',
    'load_si',
    'load_ti',
    'load_li',
    'load_people',
    'unload_si',
    'unload_ti',
    'unload_li',
    'unload_people',
    'buy_si',
    'buy_ti',
    'buy_li',
    'buy_fuel',
    'colonize_min_hab',
    'colonize_min_ti',
    'colonize_min_li',
    'colonize_min_si',
    ]

variable_maxes = [
    'load_si',
    'load_ti',
    'load_li',
    'load_people',
    'unload_si',
    'unload_ti',
    'unload_li',
    'unload_people',
    'buy_si',
    'buy_ti',
    'buy_li',
    'buy_fuel',
]

""" Default values (default, min, max)  """
__defaults = {
    'order_last_screen': 'fleets',
    'order_fleet_index': (-1, -1, sys.maxsize),
    'order_index': (-1, -1, sys.maxsize),
    'options_orders_depart': depart_options,
    'options_orders_standoff': standoff_options,
    'topbar': [],
    'orders_location_name': '',
    'orders_set_deepspace': False,
    'order_set_deepspace': [],
    'orders_x_max': (0.0, -sys.maxsize, sys.maxsize),
    'orders_x': (0.0, -sys.maxsize, sys.maxsize),
    'orders_x_min': (0.0, -sys.maxsize, sys.maxsize),
    'orders_y_max': (0.0, -sys.maxsize, sys.maxsize),
    'orders_y': (0.0, -sys.maxsize, sys.maxsize),
    'orders_y_min': (0.0, -sys.maxsize, sys.maxsize),
    'orders_z_max': (0.0, -sys.maxsize, sys.maxsize),
    'orders_z': (0.0, -sys.maxsize, sys.maxsize),
    'orders_z_min': (0.0, -sys.maxsize, sys.maxsize),
    #'order_waypoint_display': [],
}


""" Order Screen """
class Orders(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        # Load the screen with the order
        if action.startswith('load='):
            self.order_last_screen = action.split('=')[1].split(';')[0]
            self.order_fleet_index = action.split('=')[1].split(';')[1]
            self.order_index = action.split('=')[1].split(';')[2]
            if self.order_index == -1:
                # create order
                fleet = self.player.fleets[self.order_fleet_index]
                fleet.orders.append(Order())
                self.order_index = len(fleet.orders) - 1
            for item in separate_display:
                self['orders_' + item + '_display'] = self.display(item)
            for item in variable_maxes:
                self['orders_' + item + '_max'] = self.find_max(item)
            for key in Order.defaults:
                order = self.player.fleets[self.order_fleet_index].orders[self.order_index]
                if key == 'location':
                    continue
                self['orders_' + key] = order[key]
            # Special handling for location
            if order.location.reference:
                self.orders_location_name = 'some place'
            else:
                self.orders_set_deepspace = True
                self.orders_location_name = 'Deep Space'
            # Set x/y/z min/max
            print('orders printing self.player.game.__dict__:')
            for key in Game.defaults:
                print(' * ', key, ':', self.player.game[key])
            self.orders_x_min = self.player.game.x * -1.0
            self.orders_x_max = self.player.game.x * 1.0
            self.orders_x = order.location.x
            self.orders_y_min = self.player.game.y * -1.0
            self.orders_y_max = self.player.game.y * 1.0
            self.orders_y = order.location.y
            self.orders_z_min = self.player.game.z * -1.0
            self.orders_z_max = self.player.game.z * 1.0
            self.orders_z = order.location.z
        # Change the location
        print('orders printing self.__dict__:')
        for key in self.__dict__:
            print(' * ', key, ':', self[key])
        if self.orders_set_deepspace == True:
            print('setting deepspace')
            self.orders_location_name = 'Deep Space'
        # Store updates back to the order
        if self.order_fleet_index != -1 and self.order_index != -1:
            order = self.player.fleets[self.order_fleet_index].orders[self.order_index]
            for key in Order.defaults:
                if key == 'location':
                    if self.orders_location_name == 'Deep Space':
                        order[key] = Location(self.orders_x, self.orders_y, self.orders_z)
                    continue
                order[key] = self['orders_' + key]
            # Set the x/y/z back to what's actually in order
            self.orders_x = order.location.x
            self.orders_y = order.location.y
            self.orders_z = order.location.z
        # Topbar
        self.topbar.append('<i class="button far fa-times-circle"')
        if self.order_last_screen != '':
            self.topbar[-1] += ' title="Return to ' + str(self.order_last_screen) + ' screen" onclick="show_screen(\'' + str(self.order_last_screen) + '\')'
            if self.order_last_screen == 'fleets':
                self.topbar[-1] += ', post(\'fleets\', \'?select_' + str(self.order_fleet_index) + '\')'
            self.topbar[-1] += '">Back</i>'
        else:
            self.topbar[-1] += ' title="Close Orders screen" onclick="show_screen(null)">Close</i>'
        # set waypoint display
        self.order_set_deepspace.append('<td colspan="2">Set to Deepspace Coordinate</td>'+'<td><input id="orders_set_deepspace" type="checkbox" onchange="post(\'orders\')"/></td>')
        self.order_set_deepspace.append('<td>X</td>'+'<td colspan="2"><input id="orders_x" type="number" min="'+str(self.orders_x_min)+'" max="'+str(self.orders_x_max)+'" onchange="post(\'orders\')"/></td>')
        self.order_set_deepspace.append('<td>Y</td>'+'<td colspan="2"><input id="orders_y" type="number" min="'+str(self.orders_y_min)+'" max="'+str(self.orders_y_max)+'" onchange="post(\'orders\')"/></td>')
        self.order_set_deepspace.append('<td>Z</td>'+'<td colspan="2"><input id="orders_z" type="number" min="'+str(self.orders_z_min)+'" max="'+str(self.orders_z_max)+'" onchange="post(\'orders\')"/></td>')
        print('orders printing, self.orders_set_deepspace:', self.orders_set_deepspace)

    def display(self, item):
        if item == 'speed':
            if self['orders_' + item] == -2:
                return 'stargate only'
            elif self['orders_' + item] == -1:
                return 'auto'
            elif self['orders_' + item] == 0:
                return 'stopped'
            else:
                return str(self['orders_' + item])
        elif 'hab' in item:
            return str(self['orders_' + item]) + '%'
        elif 'min' in item:
            return str(self['orders_' + item] / 100)
        elif self['orders_' + item] == -1:
            if 'unload' in item:
                return 'unload all'
            elif 'load' in item:
                return 'load all available'
            elif 'buy' in item:
                return 'buy all allowed'
        elif 'people' in item:
            return str(self['orders_' + item]) + 'kT'
        else:
            return str(self['orders_' + item])

    def find_max(self, item):
        if self.order_fleet_index != -1:
            if 'fuel' in item:
                return self.player.fleets[self.order_fleet_index].stats.fuel_max
            else:
                return self.player.fleets[self.order_fleet_index].stats.cargo_max
                

for key in Order.defaults:
    __defaults['orders_' + key] = Order.defaults[key]

Orders.set_defaults(Orders, __defaults, sparse_json=False)
