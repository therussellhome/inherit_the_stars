import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    # User controls
    'energy_minister_construction_percent': [90, 0, 100],
    'energy_minister_mattrans_percent': [0, 0, 100],
    'energy_minister_mattrans_use_surplus': [False],
    'energy_minister_research_percent': [10, 0, 100],
    'energy_minister_research_use_surplus': [False],
    # Energy forecast for next year for display on GUI
    'energy_minister_forecast': [0, 0, sys.maxsize],
    # Historical energy usage by year
    'energy_minister_historical_ship': [[]],
    'energy_minister_historical_planetary': [[]],
    'energy_minister_historical_baryogenesis': [[]],
    'energy_minister_historical_mattrans': [[]],
    'energy_minister_historical_research': [[]],
    'energy_minister_historical_trade': [[]],
    # Internal game variables
    'construction_budget': [0, -sys.maxsize, sys.maxsize],
    'mattrans_budget': [0, -sys.maxsize, sys.maxsize],
    'research_budget': [0, -sys.maxsize, sys.maxsize],
    'unallocated_budget': [0, -sys.maxsize, sys.maxsize],
}

""" Represent 'energy_allocaion' """
class EnergyMinister(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Allocated the energy budget """
    def allocate_budget(self, total):
        # Add empty values to historicals
        self.energy_minister_forecast = total
        self.energy_minister_historical_ship.append(0)
        self.energy_minister_historical_planetary.append(0)
        self.energy_minister_historical_baryogenesis.append(0)
        self.energy_minister_historical_mattrans.append(0)
        self.energy_minister_historical_research.append(0)
        self.energy_minister_historical_trade.append(0)
        # Calculate energy allocations
        self.unallocated_budget = total
        for category in ['construction', 'mattrans', 'research']:
            allocation = min(round(total * getattr(self, 'energy_minister_' + category + '_percent') / 100), self.unallocated_budget)
            setattr(self, category + '_budget', allocation)
            self.unallocated_budget -= allocation

    """ Check if budget is available """
    def check_budget(self, sub_category, request):
        return self.spend_budget(sub_category, request, True)

    """ Request to spend energy for a category """
    def spend_budget(self, sub_category, request, check=False):
        category = sub_category
        # Pull from the correct budget category
        if sub_category in ['ship', 'planetary', 'baryogenesis']:
            category = 'construction'
            budget = self.construction_budget
        elif category == 'mattrans':
            budget = self.mattrans_budget
            if self.energy_minister_mattrans_use_surplus:
                budget += self.construction_budget
        elif category == 'research':
            budget = self.research_budget
            if self.energy_minister_research_use_surplus:
                budget += self.construction_budget
                budget += self.mattrans_budget
        # All other categories pull from the unallocated budget and surplus
        else:
            category = 'unallocated'
            budget = self.unallocated_budget
            budget += self.construction_budget
            budget += self.mattrans_budget
            budget += self.research_budget
        # If not enough budget then adjust request
        if request > budget:
            request = budget
        if not check:
            historical = getattr(self, 'energy_minister_historical_' + sub_category)
            historical[-1] += request
            setattr(self, 'energy_minister_historical_' + sub_category, historical)
            budget = getattr(self, category + '_budget') - request
            setattr(self, category + '_budget', budget)
        # Return approved or adjusted request
        return request


EnergyMinister.set_defaults(EnergyMinister, __defaults)
