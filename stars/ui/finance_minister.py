from .playerui import PlayerUI


""" Default values (default, min, max)  """
__defaults = {
    'finance_constuction': [''],
    'finance_mattrans': [''],
    'finance_research': [''],
    'finance_other': [''],
    'finance_construction_percent': [65, 0, 100],
    'finance_mattrans_percent': [10, 0, 100],
    'finance_reserch_percent': [15, 0, 100], 
    'finance_matrans_use_surplus': [True],
    'finance_research_use_surplus': [False],
    'finance_slider': [[65, 75, 90]],
    'finance_queue': [[]],
    'finance_buildable': [[]],
#    'finance_': [''],
}


""" """
class FinanceMinister(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if not self.player:
            return
        values = ['finance_construction_percent', 'finance_mattrans_percent', 'finance_reserch_percent', 'finance_matrans_use_surplus', 'finance_research_use_surplus']
        if action == 'reset':
            for value in values:
                self[value] = self.player()[value]
        """ save """
        self.finance_construction_percent = self.finance_slider[0]
        self.finance_mattrans_percent = self.finance_slider[1] - self.finance_slider[0]
        self.finance_mattrans_percent = self.finance_slider[2] - self.finance_slider[1]
        for value in values:
            self.player()[value] = self[value]
        """ set display values """
        self.finance_constuction = '<i class="fa-bolt>' + str(self.player().finance_construction_percent * self.player().prodict_budget() / 100) + '</i>'
        self.finance_mattrans = '<i class="fa-bolt>' + str(self.player().finance_mattrans_percent * self.player().prodict_budget() / 100) + '</i>'
        self.finance_research = '<i class="fa-bolt>' + str(self.player().finance_research_percent * self.player().prodict_budget() / 100) + '</i>'
        self.finance_other = '<i class="fa-bolt>' + str((self.player().finance_construction_percent - self.player().finance_research_percent - self.player().finance_mattrans_percent) * self.player().prodict_budget() / 100) + '</i>'
        


FinanceMinister.set_defaults(FinanceMinister, __defaults, sparse_json=False)
