from .playerui import PlayerUI
from ..build_ship import BuildShip
from ..reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'finance_constuction': '',
    'finance_mattrans': '',
    'finance_research': '',
    'finance_other': '',
    'finance_construction_percent': (65.0, 0.0, 100.0),
    'finance_mattrans_percent': (10.0, 0.0, 100.0),
    'finance_research_percent': (15.0, 0.0, 100.0), 
    'finance_mattrans_use_surplus': True,
    'finance_research_use_surplus': False,
    'finance_slider': [65.0, 75.0, 90.0],
    'finance_queue': [],
    'finance_buildable': [],
    'options_finance_planet': [],
    'finance_planet': '',
#    'finance_': '',
}


""" """
class FinanceMinister(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        values = ['finance_construction_percent', 'finance_mattrans_percent', 'finance_research_percent', 'finance_mattrans_use_surplus', 'finance_research_use_surplus']
        if action[:4] == 'add=':
            i = int(action[4:])
            for p in self.player.planetary_minister_map:
                if p.ID == self.finance_planet:
                    self.player.build_queue.append(BuildShip(ship_design=self.player.ship_designs[i]))
                    #TODO , player=self.player, planet=Reference('Sun')
                    break
            else:
                self.user_alerts.append(self.finance_planet + ' is an invaled ID')
        if action[:4] == 'del=':
            del self.player.build_queue[int(action[4:])]
        if action == 'show_screen':
            for value in values:
                self[value] = self.player[value]
            self.finance_slider[0] = self.player.finance_construction_percent
            self.finance_slider[1] = self.player.finance_mattrans_percent + self.finance_slider[0]
            self.finance_slider[2] = self.player.finance_research_percent + self.finance_slider[1]
        """ save """
        self.finance_construction_percent = self.finance_slider[0]
        self.finance_mattrans_percent = self.finance_slider[1] - self.finance_slider[0]
        self.finance_research_percent = self.finance_slider[2] - self.finance_slider[1]
        for value in values:
            self.player[value] = self[value]
        """ set display values """
        self.finance_construction = '<i class="fa-bolt">' + str(round(self.player.finance_construction_percent * self.player.predict_budget() / 100)) + '</i>'
        self.finance_mattrans = '<i class="fa-bolt">' + str(round(self.player.finance_mattrans_percent * self.player.predict_budget() / 100)) + '</i>'
        self.finance_research = '<i class="fa-bolt">' + str(round(self.player.finance_research_percent * self.player.predict_budget() / 100)) + '</i>'
        self.finance_other = '<i class="fa-bolt">' + str(round((((100-self.player.finance_construction_percent) - self.player.finance_research_percent) - self.player.finance_mattrans_percent) * self.player.predict_budget() / 100)) + '</i>'
        for planet in self.player.planets:
            self.options_finance_planet.append(planet.ID)
        # build queue
        queue = self.player.build_queue
        for i in range(len(queue)):
            item = queue[i]
            self.finance_queue.append('<td rowspan="2">' + item.to_html() + '</td><td rowspan="2">' + str(1 - item.cost.percent(item.spent + item.cost)) + '</td>'
                + '<td rowspan="2"><i class="button far fa-trash-alt" title="Remove from queue" onclick="post(\'finance_minister\', \'?del=' + str(i) + '\')"></i></td>')
            self.finance_queue.append('<td></td>')
            #TODO <td>' + item.planet.time_til_html(item.cost.to_html(), queue, i)[0] + '</td><td rowspan="2">' + item.planet.ID + '</td>  ' + item.planet.time_til_html(item.cost.to_html(), queue, i)[1] + '
        # buildables
        queue = self.player.ship_designs
        self.finance_buildable.append('<td colspan="3"><select id="finance_planet" style="width: 100%" onchange="post(\'finance_minister\')"/></td>')
        for i in range(len(queue)):
            item = BuildShip(ship_design = queue[i])
            self.finance_buildable.append('<td>' + item.to_html() + '</td><td>' + item.cost.to_html() + '</td>'
                + '<td><i class="button fas fa-cart-plus" title="Add to queue" onclick="post(\'finance_minister\', \'?add=' + str(i) + '\')"></i></td>')

FinanceMinister.set_defaults(FinanceMinister, __defaults, sparse_json=False)
