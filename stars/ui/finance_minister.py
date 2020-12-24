from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'finance_constuction': [''],
    'finance_mattrans': [''],
    'finance_research': [''],
    'finance_other': [''],
    'finance_construction_percent': [65.0, 0.0, 100.0],
    'finance_mattrans_percent': [10.0, 0.0, 100.0],
    'finance_research_percent': [15.0, 0.0, 100.0], 
    'finance_mattrans_use_surplus': [True],
    'finance_research_use_surplus': [False],
    'finance_slider': [[65.0, 75.0, 90.0]],
    'finance_queue': [[]],
    'finance_buildable': [[]],
#    'finance_': [''],
}


""" """
class FinanceMinister(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player():
            return
        values = ['finance_construction_percent', 'finance_mattrans_percent', 'finance_research_percent', 'finance_mattrans_use_surplus', 'finance_research_use_surplus']
        for value in values:
            print(value + ':', self.player()[value])
        if action == 'show_screen':
            for value in values:
                self[value] = self.player()[value]
            self.finance_slider[0] = self.player().finance_construction_percent
            self.finance_slider[1] = self.player().finance_mattrans_percent + self.finance_slider[0]
            self.finance_slider[2] = self.player().finance_research_percent + self.finance_slider[1]
        """ save """
        self.finance_construction_percent = self.finance_slider[0]
        self.finance_mattrans_percent = self.finance_slider[1] - self.finance_slider[0]
        self.finance_research_percent = self.finance_slider[2] - self.finance_slider[1]
        for value in values:
            self.player()[value] = self[value]
        print(self.__dict__)
        """ set display values """
        self.finance_construction = '<i class="fa-bolt">' + str(round(self.player().finance_construction_percent * self.player().predict_budget() / 100)) + '</i>'
        self.finance_mattrans = '<i class="fa-bolt">' + str(round(self.player().finance_mattrans_percent * self.player().predict_budget() / 100)) + '</i>'
        self.finance_research = '<i class="fa-bolt">' + str(round(self.player().finance_research_percent * self.player().predict_budget() / 100)) + '</i>'
        self.finance_other = '<i class="fa-bolt">' + str(round((((100-self.player().finance_construction_percent) - self.player().finance_research_percent) - self.player().finance_mattrans_percent) * self.player().predict_budget() / 100)) + '</i>'
        


FinanceMinister.set_defaults(FinanceMinister, __defaults, sparse_json=False)
