from .playerui import PlayerUI
from ..reference import Reference
from ..waypoint import Waypoint as Waypoint_2


""" Default values (default, min, max)  """
__defaults = {
    'last_screen': '',
    'fleet_index': '',
    'topbar': '',
}

""" Foregin misister shows current relationships / treaties and pending treaties """
class Waypoint(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        # get last screen
        if action.startswith('screen='):
            self.last_screen = action.split('=')[1]
        # get fleet value
        if action.startswith('fleet_index='):
            self.fleet_index = action.split('=')[1]
        self.topbar = ['<i class="button far fa-times-circle" title="Return to ' + str(self.last_screen) + ' screen" onclick="show_screen(\'' + str(self.last_screen) + '\')']
        if last_screen == 'fleets':
            self.topbar[0] += ', post(\'' + str(self.last_screen) + '\', \'?select_' + str(self.fleet_index) + ')'
        self.topbar[0] += '"></i>'
        buttons = '<td rowspan="2"></td>' \
            + '<td rowspan="2"><i class="button far fa-trash-alt" title="Cancel" onclick="post(\'foreign_minister\', \'?reject=' + treaty.name + '\')"></i></td>'
        if treaty.status == 'pending':
            buttons = '<td rowspan="2"><i class="button far fa-check-circle" title="Accept" onclick="post(\'foreign_minister\', \'?accept=' + treaty.name + '\')"></i></td>' \
                + '<td rowspan="2"><i class="button far fa-trash-alt" title="Reject" onclick="post(\'foreign_minister\', \'?reject=' + treaty.name + '\')"></i></td>'
        self.foreign_treaties.append('<td rowspan="2" style="color: silver; font-size: 150%">' + self._display_relationship(treaty.relation) + '</td>'
            + '<td>Buy</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.buy_ti) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.buy_li) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.buy_si) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.buy_fuel) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.buy_gate) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.buy_hyper_denial) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.buy_intel) + '</td>'
            + buttons)
        self.foreign_treaties.append('<td>Sell</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.sell_ti) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.sell_li) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.sell_si) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.sell_fuel) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.sell_gate) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.sell_hyper_denial) + '</td>'
            + '<td style="font-size: 80%">' + self._display_energy(treaty.sell_intel) + '</td>')

ForeignMinister.set_defaults(ForeignMinister, __defaults, sparse_json=False)
