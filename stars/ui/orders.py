from .playerui import PlayerUI
from ..reference import Reference
from ..order import Order, depart_options, standoff_options, seperate_display, veriable_maxes
import sys
import copy

""" Default values (default, min, max)  """
__defaults = {
    'order_last_screen': 'fleets',
    'order_fleet_index': (-1, -1, sys.maxsize),
    'order_index': (-1, -1, sys.maxsize),
    'options_orders_depart': depart_options,
    'options_orders_standoff': standoff_options,
    'topbar': [],
}


""" Foregin misister shows current relationships / treaties and pending treaties """
class Orders(PlayerUI):
    def __init__(self, actions, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        for item in seperate_display:
            self['orders_' + item + '_display'] = self.display(item)
        for item in veriable_maxes:
            self['orders_' + item + '_max'] = self.find_max(item)
        for action in actions.split(';'):
            # get fleet value
            if action.startswith('fleet_index='):
                self.order_fleet_index = str(action.split('=')[1])
            if action.startswith('order='):
                self.order_index = str(action.split('=')[1])
            if action == 'start' and self.order_fleet_index != -1 and self.order_index != -1:
                order = self.player().fleets[self.order_fleet_index].orders[self.order_index]
                for key in Order.defaults:
                    self['orders_' + key] = order[key]
            # get last screen
            if action.startswith('screen='):
                self.order_last_screen = str(action.split('=')[1])
            if self.order_last_screen != '' and len(self.topbar) == 0:
                self.topbar.append('<i class="button far fa-times-circle" title="Return to ' + str(self.order_last_screen) + ' screen" onclick="show_screen(\'' + str(self.order_last_screen) + '\')')
                if self.order_last_screen == 'fleets':
                    self.topbar[-1] += ', post(\'' + str(self.order_last_screen) + '\', \'?select_' + str(self.order_fleet_index) + '\')'
                self.topbar[-1] += '">Back</i>'
            self.order_fleet_index != -1
        if self.order_fleet_index != -1 and self.order_index != -1:
            order = self.player().fleets[self.order_fleet_index].orders[self.order_index]
            for key in Order.defaults:
                order[key] = self['orders_' + key]
            #print(order.__dict__, '\n')

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
                return self.player().fleets[self.order_fleet_index].__cache__['fuel_max']
            else:
                return self.player().fleets[self.order_fleet_index].__cache__['cargo_max']
                

for key in Order.defaults:
    __defaults['orders_' + key] = Order.defaults[key]

Orders.set_defaults(Orders, __defaults, sparse_json=False)
