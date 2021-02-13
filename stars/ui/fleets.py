from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'fleet_list': [],
    'fleet_index': 0,
    'ships': [],
    'waypoints': [],
}


""" """
class Fleets(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        self.fleet_list.append('<th></th><th></th>'
                + '<th><i title="Name of the Fleet">Name</i></th>'
                + '<th><i title="X Cordinate">X</i></th>'
                + '<th><i title="Y Cordinate">Y</i></th>'
                + '<th><i title="Z Cordinate">Z</i></th>'
                + '<th><i class="fa-free-code-camp" title="Fuel">Fuel</i></th>'
                + '<th><i title="KT of People in fleet"></i>People</th>'
                + '<th><i class="ti" title="Titanium">in </i></th>'
                + '<th><i class="li" title="Lithium">in </i></th>'
                + '<th><i class="si" title="Silicon">in </i></th>')
        for fleet in self.player().fleets:
            self.fleets_list.append('<tr>'
                + '<td>' + fleet.location.x + '</td>'
                + '<td>' + fleet.location.y + '</td>'
                + '<td>' + fleet.location.z + '</td>'
                + '<td>' + fleet.get_fuel()[0] + '</td>'
                + '<td>' + fleet.get_cargo()[0].people + '</td>'
                + '<td>' + fleet.get_cargo()[0].titanium + '</td>'
                + '<td>' + fleet.get_cargo()[0].lithium + '</td>'
                + '<td>' + fleet.get_cargo()[0].silicon + '</td>' + '</tr>')
        self.ships.append('<th></th><th></th>'
                + '<th><i title="Name of Ship Design">Ship Design</i></th>'
                + '<th><i class="fa-free-code-camp" title="Fuel">Fuel</i></th>'
                + '<th><i title="KT of People in fleet"></i>People</th>'
                + '<th><i class="ti" title="Titanium">in </i></th>'
                + '<th><i class="li" title="Lithium">in </i></th>'
                + '<th><i class="si" title="Silicon">in </i></th>'
                + '<th><i title="Intel Sharing"></i></th>')
        '''if len(self.player().fleets) > 0:
            for ship in self.player().fleets[self.fleet_index]:
                self.ships.append('<tr>'
                    + '<td>' + ship.location.x + '</td>'
                    + '<td>' + fleet.location.y + '</td>'
                    + '<td>' + fleet.location.z + '</td>'
                    + '<td>' + ship.fuel + '</td>'
                    + '<td>' + ship.cargo.people + '</td>'
                    + '<td>' + ship.cargo.titanium + '</td>'
                    + '<td>' + ship.cargo.lithium + '</td>'
                    + '<td>' + ship.cargo.silicon + '</td>' + '</tr>')'''
        self.waypoints.append('<th></th><th></th>'
                + '<th><i title="Name of the Fleet">Name</i></th>'
                + '<th><i title="X Cordinate">X</i></th>'
                + '<th><i title="Y Cordinate">Y</i></th>'
                + '<th><i title="Z Cordinate">Z</i></th>'
                + '<th><i class="fa-free-code-camp" title="Fuel">Fuel</i></th>'
                + '<th><i title="KT of People in fleet"></i>People</th>'
                + '<th><i class="ti" title="Titanium">in </i></th>'
                + '<th><i class="li" title="Lithium">in </i></th>'
                + '<th><i class="si" title="Silicon">in </i></th>')
        for fleet in self.player().fleets:
            self.fleets_list.append('<tr>'
                + '<td>' + fleet.location.x + '</td>'
                + '<td>' + fleet.location.y + '</td>'
                + '<td>' + fleet.location.z + '</td>'
                + '<td>' + fleet.get_fuel()[0] + '</td>'
                + '<td>' + fleet.get_cargo()[0].people + '</td>'
                + '<td>' + fleet.get_cargo()[0].titanium + '</td>'
                + '<td>' + fleet.get_cargo()[0].lithium + '</td>'
                + '<td>' + fleet.get_cargo()[0].silicon + '</td>' + '</tr>')
        


Fleets.set_defaults(Fleets, __defaults, sparse_json=False)
