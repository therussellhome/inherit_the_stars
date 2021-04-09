from .playerui import PlayerUI
from ..reference import Reference
from ..waypoint import Waypoint, depart_options, standoff_options, seperate_display, cargo_options, veriable_maxes
import sys
import copy

""" Default values (default, min, max)  """
__defaults = {
    'waypoint_last_screen': 'fleets',
    'waypoint_fleet_index': (-1, -1, sys.maxsize),
    'waypoint_index': (-1, -1, sys.maxsize),
    'options_waypoints_depart': depart_options,
    'options_waypoints_standoff': standoff_options,
    'topbar': [],
}


""" Foregin misister shows current relationships / treaties and pending treaties """
class Waypoints(PlayerUI):
    def __init__(self, actions, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        for item in seperate_display:
            self['waypoints_' + item + '_display'] = self.display(item)
        for item in veriable_maxes:
            self['waypoints_' + item + '_max'] = self.find_max(item)
        for action in actions.split(';'):
            # get fleet value
            if action.startswith('fleet_index='):
                self.waypoint_fleet_index = str(action.split('=')[1])
            if action.startswith('waypoint='):
                self.waypoint_index = str(action.split('=')[1])
            if action == 'start' and self.waypoint_fleet_index != -1 and self.waypoint_index != -1:
                waypoint = self.player().fleets[self.waypoint_fleet_index].waypoints[self.waypoint_index]
                for key in Waypoint.defaults:
                    self['waypoints_' + key] = waypoint[key]
            # get last screen
            if action.startswith('screen='):
                self.waypoint_last_screen = str(action.split('=')[1])
            if self.waypoint_last_screen != '' and len(self.topbar) == 0:
                self.topbar.append('<i class="button far fa-times-circle" title="Return to ' + str(self.waypoint_last_screen) + ' screen" onclick="show_screen(\'' + str(self.waypoint_last_screen) + '\')')
                if self.waypoint_last_screen == 'fleets':
                    self.topbar[-1] += ', post(\'' + str(self.waypoint_last_screen) + '\', \'?select_' + str(self.waypoint_fleet_index) + '\')'
                self.topbar[-1] += '">Back</i>'
            self.waypoint_fleet_index != -1
        if self.waypoint_fleet_index != -1 and self.waypoint_index != -1:
            waypoint = self.player().fleets[self.waypoint_fleet_index].waypoints[self.waypoint_index]
            for key in Waypoint.defaults:
                waypoint[key] = self['waypoints_' + key]
            #print(waypoint.__dict__, '\n')

    def display(self, item):
        if item == 'speed':
            if self['waypoints_' + item] == -2:
                return 'auto'
            elif self['waypoints_' + item] == -1:
                return 'use stargate'
            elif self['waypoints_' + item] == 0:
                return 'stopped'
            else:
                return str(self['waypoints_' + item])
        elif 'hab' in item:
            return str(self['waypoints_' + item]) + '%'
        elif 'min' in item:
            return str(self['waypoints_' + item] / 100)
        elif self['waypoints_' + item] == -1:
            if 'unload' in item:
                return 'unload all'
            elif 'load' in item:
                return 'load all available'
            elif 'buy' in item:
                return 'buy all allowed'
        elif 'people' in item:
            return str(self['waypoints_' + item]) + 'kT'
        else:
            return str(self['waypoints_' + item])

    def find_max(self, item):
        if self.waypoint_fleet_index != -1:
            if 'fuel' in item:
                return self.player().fleets[self.waypoint_fleet_index].get_fuel()[1]
            else:
                return self.player().fleets[self.waypoint_fleet_index].get_cargo()[1]
                

for key in Waypoint.defaults:
    __defaults['waypoints_' + key] = Waypoint.defaults[key]

Waypoints.set_defaults(Waypoints, __defaults, sparse_json=False)
