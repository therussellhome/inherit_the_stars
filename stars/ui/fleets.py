from .playerui import PlayerUI
import sys

""" Default values (default, min, max)  """
__defaults = {
    'fleet_list': [],
    'other_ships': [],
    'fleet_index': (0, 0, sys.maxsize),
    'ships': [],
    'fleet_waypoints': [],
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
                + '<td>' + str(fleet.get_fuel()[0]) + '</td>'
                + '<td>' + str(fleet.get_cargo()[0].people) + '</td>'
                + '<td>' + str(fleet.get_cargo()[0].titanium) + '</td>'
                + '<td>' + str(fleet.get_cargo()[0].lithium) + '</td>'
                + '<td>' + str(fleet.get_cargo()[0].silicon) + '</td>' + '</tr>')
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
        self.fleet_waypoints.append('<th><i title="Fleet orders">Actions</i></th>'
                + '<th></th>' + '<th></th>' + '<th></th>' + '<th></th>' + '<th></th>'
                + '<th><i title="X Cordinate">X</i></th>'
                + '<th><i title="Y Cordinate">Y</i></th>'
                + '<th><i title="Z Cordinate">Z</i></th>')
        #for i in self.player().fleets:
        if len(self.player().fleets) > 0:
            for I in range(len(self.player().fleets[self.fleet_index].waypoints)):
                waypoint = self.player().fleets[self.fleet_index].waypoints[I]
                shown = ''
                for i in range(5):
                    if i >= len(waypoint.actions):
                        shown += '<td></td>'
                    else:
                        shown += '<td>' + str(waypoint.actions[i]) + '</td>'
                shown += str('<td>' + str(waypoint.location.x) + '</td>'
                            + '<td>' + str(waypoint.location.y) + '</td>'
                            + '<td>' + str(waypoint.location.z) + '</td>')
                self.fleet_waypoints.append('<tr>'
                    + '<td><i class="button fas fa-edit" title="Select waypoint" onclick="show_screen(\'waypoints\'), post(\'waypoints\', \'?waypoint=' + str(I) + ';fleet_index=' + str(self.fleet_index) + ';screen=fleets\')"></td>'
                    + shown + '</tr>')
        


Fleets.set_defaults(Fleets, __defaults, sparse_json=False)
