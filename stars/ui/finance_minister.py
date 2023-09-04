from .playerui import PlayerUI
from ..buships import BuShips
from ..reference import Reference
from ..cost import Cost


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
            ID = action[4:]
            if not self.finance_planet == '':
                for design in self.player.ship_designs:
                    if design.ID == ID:
                        self.player.buships.append(BuShips(ship_design=design, planet=Reference('Planet/' + self.finance_planet)))
        if action[:4] == 'del=':
            to_del = action[4:]
            for buships in self.player.buships:
                if buships.ID == to_del:
                    self.player.buships.remove(buships)
                    break
        if action == 'show_screen':
            for value in values:
                self[value] = self.player[value]
            self.finance_planet = self.player.planets[0]
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
        self.finance_construction = '<i class="fa-bolt">' + str(round(self.player.predict_income('construction') * 100)) + '</i>'
        self.finance_mattrans = '<i class="fa-bolt">' + str(round(self.player.predict_income('mattrans') * 100)) + '</i>'
        self.finance_research = '<i class="fa-bolt">' + str(round(self.player.predict_income('research') * 100)) + '</i>'
        self.finance_other = '<i class="fa-bolt">' + str(round(self.player.predict_income('other') * 100)) + '</i>'
        for planet in self.player.planets:
            self.options_finance_planet.append(planet.ID)
        # build queue #TODO add way to rearrage build queue without removing in progres items
        self.finance_queue = ['<td>name</td><td>cost remaining</td><td>time left</td><td>limiting factor</td><td>% complete</td><td>planet</td><td></td>']
        total_cost = Cost()
        for item in self.player.buships:
            total_cost += item.cost
            self.finance_queue.append('<td>' + item.ship_design.ID + '</td>' + item.planet.time_til_html(total_cost, item.cost) + '</td><td>' + str(item.percent) + '</td><td>' + item.planet.ID + '</td>'
                + '<td><i class="button far fa-trash-alt" title="Remove from queue" onclick="post(\'finance_minister\', \'?del=' + item.ID + '\')"></i></td>')
        # buildables
        buildables = self.player.ship_designs
        self.finance_buildable.append('<td colspan="3"><select id="finance_planet" style="width: 100%" onchange="post(\'finance_minister\')"/></td>')
        for i in range(len(buildables)):
            item = buildables[i]
            self.finance_buildable.append('<td>' + item.ID + '</td><td>' + item.cost.to_html() + '</td>'
                + '<td><i class="button fas fa-cart-plus" title="Add to queue" onclick="post(\'finance_minister\', \'?add=' + str(item.ID) + '\')"></i></td>')

FinanceMinister.set_defaults(FinanceMinister, __defaults, sparse_json=False)
