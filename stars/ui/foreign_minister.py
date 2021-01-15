from .playerui import PlayerUI
from ..reference import Reference
from ..treaty import Treaty, TREATY_BUY_SELL_FIELDS


""" Default values (default, min, max)  """
__defaults = {
    'foreign_treaties': [],
    'foreign_other_player': '',
    'foreign_relation_is_team': False,
    'foreign_relation_is_neutral': True,
    'foreign_relation_is_enemy': False,
}

# Add all keys from the treaty object for the negotiation table
for key in TREATY_BUY_SELL_FIELDS:
    __defaults['foreign_' + key] = Treaty.defaults[key]
    __defaults['foreign_' + key + '_display'] = ['Never']


""" Foregin misister shows current relationships / treaties and pending treaties """
class ForeignMinister(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        # Reject a treaty
        if action.startswith('reject='):
            reject = action.split('=', 2)[1]
            for t in self.player().treaties:
                if t.name == reject:
                    t.status = 'rejected'
        # Propose a treaty
        elif action.startswith('propose='):
            other_player = Reference('Player/' + action.split('=', 2)[1])
            treaty = self.player().get_treaty(other_player, True)
            if not treaty:
                treaty = self.player().get_treaty(other_player, False)
            self.foreign_other_player = other_player.name
            self.foreign_relation_is_team = False
            self.foreign_relation_is_neutral = False
            self.foreign_relation_is_enemy = False
            if treaty.relation == 'team':
                self.foreign_relation_is_team = True
            elif treaty.relation == 'neutral':
                self.foreign_relation_is_neutral = True
            else:
                self.foreign_relation_is_enemy = True
            for f in TREATY_BUY_SELL_FIELDS:
                self['foreign_' + f] = treaty[f]
        # Save the proposal
        elif action == 'save' and self.foreign_other_player != '':
            other_player = Reference('Player/' + self.foreign_other_player)
            treaty = self.player().get_treaty(other_player, True)
            if treaty:
                treaty.status = 'rejected'
            treaty = Treaty(other_player=other_player)
            if self.foreign_relation_is_team:
                treaty.relation = 'team'
            elif self.foreign_relation_is_enemy:
                treaty.relation = 'enemy'
                treaty.status = 'active'
            for f in TREATY_BUY_SELL_FIELDS:
                treaty[f] = self['foreign_' + f]
            self.player().treaties.append(treaty)
        # Treaties header
        self.foreign_treaties.append('<th></th><th></th>'
            + '<th><i class="ti" title="Titanium">1</i></th>'
            + '<th><i class="li" title="Lithium">1</i></th>'
            + '<th><i class="si" title="Silicon">1</i></th>'
            + '<th><i class="fa-free-code-camp" title="Fuel">100</i></th>'
            + '<th><i style="font-size: 150%" class="fab fa-galactic-republic" title="Stargate"></i></th>'
            + '<th><i style="font-size: 150%" class="fas fa-ban" title="Hyper Denial Passage"></i></th>'
            + '<th><i style="font-size: 150%" class="fas fa-user-secret" title="Intel Sharing"></i></th>')
        # Display existing treaties
        for other_player in self.player().get_intel(by_type='Player'):
            treaty = self.player().get_treaty(other_player, False)
            self.foreign_treaties.append('<td colspan="10" style="font-size: 150%; text-align: left; border: 1px solid silver; border-right: 0">'
                + '<i class="' + other_player.race.icon + '"></i>' + other_player.name + '</td>'
                + '<td style="border: 1px solid silver; border-left: 0"><i class="button fas fa-user-edit" title="Propose Treaty" onclick="post(\'foreign_minister\', \'?propose=' + treaty.other_player.name + '\')"></i></td>')
            self._display_treaty(treaty)
            treaty = self.player().get_treaty(other_player, True)
            if treaty:
                self._display_treaty(treaty)
        # Override negotiation for team
        if self.foreign_relation_is_team:
            for f in ['gate', 'hyper_denial', 'intel']:
                self['foreign_buy_' + f] = 0
                self['foreign_sell_' + f] = 0
        # No selling to enemies
        elif self.foreign_relation_is_enemy:
            for f in ['ti', 'li', 'si', 'fuel', 'gate', 'hyper_denial', 'intel']:
                self['foreign_buy_' + f] = -10000
                self['foreign_sell_' + f] = -10000
        # Update the negotiation display
        for f in TREATY_BUY_SELL_FIELDS:
            self['foreign_' + f + '_display'] = self._display_energy(self['foreign_' + f])

    """ Build rows for a current/proposed treaty """
    def _display_treaty(self, treaty):
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

    """ Icon for the relationship """
    def _display_relationship(self, relationship):
        if relationship == 'enemy':
            return '<i class="fas fa-skull-crossbones"></i>'
        elif relationship == 'team':
            return'<i class="fas fa-handshake"></i>'
        return '<i class="fas fa-meh"></i>'

    """ Format a number as energy or - if none """
    def _display_energy(self, energy):
        if energy < 0:
            return '-'
        elif energy >= 1000:
            energy = round(energy / 1000, 2)
            if energy % 1 == 0:
                energy = int(energy)
            energy = str(energy) + 'k'
        return '<i class="fa-bolt" title="Energy">' + str(energy) + '</i>'

ForeignMinister.set_defaults(ForeignMinister, __defaults, sparse_json=False)
