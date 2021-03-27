from .playerui import PlayerUI
from ..reference import Reference
from ..waypoint import Waypoint, cargo_options
import sys
import copy

""" Default values (default, min, max)  """
__defaults = {
    'last_screen': 'fleets',
    'waypoint_fleet_index': '',
    'waypoint_index': '',
    'waypoint_data': [],
    'edit_waypoint': [],
    'topbar': [],
}


""" Foregin misister shows current relationships / treaties and pending treaties """
class Waypoints(PlayerUI):
    def __init__(self, actions, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        self.waypoints_load_cargo1_type = cargo_options
        #race = self.player().race
        #for key in Race.defaults:
        #    self['waypoints_' + key] = race[key]
        #for action in fleet.fleet_actions:
        #    for item in t
        for action in actions.split(';'):
            # get fleet value
            if action.startswith('fleet_index='):
                self.waypoint_fleet_index = str(action.split('=')[1])
            if action.startswith('waypoint='):
                self.waypoint_index = str(action.split('=')[1])
            # get last screen
            if action.startswith('screen='):
                self.last_screen = str(action.split('=')[1])
                self.topbar.append('<i class="button far fa-times-circle" title="Return to ' + str(self.last_screen) + ' screen" onclick="show_screen(\'' + str(self.last_screen) + '\')')
                if self.last_screen == 'fleets':
                    self.topbar[-1] += ', post(\'' + str(self.last_screen) + '\', \'?select_' + str(self.waypoint_fleet_index) + '\')'
                self.topbar[-1] += '">Back</i>'
        self.edit_waypoint.append('<th><i title="action">action</i></th>'
            + '<th><i title="what gets the action applied to it">recipiant</i></th>'
            + '<th><i title="amount of li, si, ti, or people to be transfered in this action">cargo1</i></th>'
            + '<th><i title="amount of li, si, ti, or people to be transfered in this action">cargo2</i></th>'
            + '<th><i title="amount of li, si, ti, or people to be transfered in this action">cargo3</i></th>'
            + '<th><i title="amount of li, si, ti, or people to be transfered in this action">cargo4</i></th>'
            + '<th><i title="amount of fuel to be transfered in this action">fuel</i></th>')
        if self.waypoint_fleet_index != '' and self.waypoint_index != '':
            waypoint = self.player().fleets[int(self.waypoint_fleet_index)].waypoints[int(self.waypoint_index)]
            self.waypoint_data.append('<tr>'
                + '<td>' + str(waypoint.location.x) +  '</td>'
                + '<td>' + str(waypoint.location.y) +  '</td>'
                + '<td>' + str(waypoint.location.z) +  '</td>' + '</tr>')
            for action in waypoint.actions:
                self.edit_waypoint.append('<tr>' + '<td>' + str(action) + '</td>'
                    + '<td class="hfill"><select id="waypoints_' + str(action) + '_cargo1" class="hfill" onchange="post(\'waypoints\')"/>'
                    + '<input id="waypoints_' + str(action) + '_cargo1" type="number" min="0" max="' + str(sys.maxsize) + '" onchange="post(\'waypoints\')"/></td>'
                    + '<td class="hfill"><select id="waypoints_' + str(action) + '_cargo2" class="hfill" onchange="post(\'waypoints\')"/>'
                    + '<input id="waypoints_' + str(action) + '_cargo2" type="number" min="0" max="' + str(sys.maxsize) + '" onchange="post(\'waypoints\')"/></td>'
                    + '<td class="hfill"><select id="waypoints_' + str(action) + '_cargo3" class="hfill" onchange="post(\'waypoints\')"/>'
                    + '<input id="waypoints_' + str(action) + '_cargo3" type="number" min="0" max="' + str(sys.maxsize) + '" onchange="post(\'waypoints\')"/></td>'
                    + '<td class="hfill"><select id="waypoints_' + str(action) + '_cargo4" class="hfill" onchange="post(\'waypoints\')"/>'
                    + '<input id="waypoints_' + str(action) + '_cargo4" type="number" min="0" max="' + str(sys.maxsize) + '" onchange="post(\'waypoints\')"/></td>'
                    + '<td class="hfill"><select id="waypoints_' + str(action) + '_fuel" class="hfill" onchange="post(\'waypoints\')"/>'
                    + '<input id="waypoints_' + str(action) + '_fuel" type="number" min="0" max="' + str(sys.maxsize) + '" onchange="post(\'waypoints\')"/></td>'
                    + '</tr>')
                if action in ['load', 'unload', 'sell', 'buy'] and action in waypoint.transfers:
                    for i in range(5):
                        if i >= len(waypoint.transfers[action]):
                            self.edit_waypoint[-1] += '<td>' + str(action) +  '</td>'
                        item = waypoint.transfers[action]
                        if item[0] == 'fuel':
                            fuel = item[1]
                    '''+ '<td>' + str(action) +  '</td>'
                    + '<td>' + str(action) +  '</td>'
                    + '<td>' + str(action) +  '</td>'
                    + '<td>' + str(action) +  '</td>'
                    + '<td>' + str(action) +  '</td>' + '</tr>')#'''
        print('last screen:', self.last_screen, 'waypoint fleet index:', self.waypoint_fleet_index, 'waypoint index:', self.waypoint_index)

Waypoints.set_defaults(Waypoints, __defaults, sparse_json=False)
