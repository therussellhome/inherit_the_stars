import sys
from math import ceil
from . import game_engine
from .defaults import Defaults
from .intel import Intel
from .planetary_minister import PlanetaryMinister
from .race import Race
from .reference import Reference
from .score import Score
from .tech_level import TechLevel, TECH_FIELDS
from .fleet import Fleet

""" Default values (default, min, max)  """
__defaults = {
    'game_name': [''], # name of game for when generating
    'player_key': [''], # used to validate the player file
    'ready_to_generate': [False],
    'date': [0.0, 0.0, sys.maxsize],
    'race': [Race()],
    'computer_player': [False],
    'seen_players': [[]],
    'intel': [{}], # map of intel objects indexed by object reference
    'messages': [[]], # list of messages from oldest to newest
    'planetary_ministers': [[PlanetaryMinister(name='New Colony Minister', new_colony_minister=True)]], # list of planetary ministers
    'score': [Score()],
    'tech_level': [TechLevel()], # current tech levels
    'research_partial': [TechLevel()], # energy spent toward next level
    'research_queue': [[]], # queue of tech items to research
    'research_field': ['<LOWEST>'], # next field to research (or 'lowest')
    'energy': [0, 0, sys.maxsize],
    'fleets': [[]],
    'tech': [[]], # tech tree
    'treaties': [{}],
    'pending_treaties': [{}],
    'energy_minister_construction_percent': [90, 0, 100],
    'energy_minister_mattrans_percent': [0, 0, 100],
    'energy_minister_mattrans_use_surplus': [False],
    'energy_minister_research_percent': [10, 0, 100],
    'energy_minister_research_use_surplus': [False],
    'historical': [{}], # map of category to value by year (not hundreth)
}

""" List of fields that are user modifable """
_player_fields = [
    'ready_to_generate',
    'planetary_ministers',
    'research_queue',
    'research_field',
    'fleets',
    'treaties',
    'energy_minister_construction_percent',
    'energy_minister_mattrans_percent',
    'energy_minister_mattrans_use_surplus',
    'energy_minister_research_percent',
    'energy_minister_research_use_surplus',
]

""" A player in a game """
class Player(Defaults):
    """ Initialize """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = self.race.name
        if 'date' not in kwargs:
            self.date = self.race.start_date
        if 'player_key' not in kwargs:
            self.player_key = str(id(self))
        game_engine.register(self)
        self.__cache__ = {}

    """ Update self from file """
    def update_from_file(self):
        global _player_fields
        p = game_engine.load_inspect('games', self.game_name + ' - ' + self.name)
        if self.player_key == p.player_key:
            for field in _player_fields:
                self[field] = p[field]

    """ Update the date """
    def next_hundreth(self):
        self.date = round(self.date + 0.01, 2)

    """ calles fleets to do actions """
    def ship_action(self, action):
        for fleet in self.fleets:
            fleet.execute(action, self)
    
    def create_fleet(self, **kwargs):
        self.fleets.append(Fleet(**kwargs))
    
    def add_fleet(self, fleet):
        self.fleets.append(fleet)
    
    def remove_fleet(self, fleet):
        self.fleets.remove(fleet)
    
    """ Return the id for use as a temporary player token """
    def token(self):
        return str(id(self))

    """ Add an intel report """
    def add_intel(self, obj, **kwargs):
        # Intentionally allowing this to fail if the object does not have a name attribute
        reference = obj.__class__.__name__ + '/' + obj.name
        if reference not in self.intel:
            self.intel[reference] = Intel(reference=reference)
        self.intel[reference].add_report(date=self.date, **kwargs)
        # If seeing a new player then capture that
        # TODO put player name in seen_players
        if 'player' in kwargs:
            reference = 'Player/' + kwargs['player']
            if reference not in self.intel:
                self.intel[reference] = Intel(reference=reference)

    """ Get intel about an object or objects """
    def get_intel(self, reference):
        if '/' in reference:
            if reference in self.intel:
                return self.intel[reference]
            return Intel()
        reports = []
        for k, i in self.intel.items():
            if k.startswith(reference + '/'):
                reports.append(i)
        return reports

    """ 'Recieve' intel reports """
    def calc_intel(self):
        # First run includes all of the stars
        if len(self.intel) == 0:
            for s in game_engine.get('Sun'):
                self.add_intel(s, name=s.name, location=s.location, color=s.get_color(), size=s.gravity)

    """ Store historical values - accumulates across the year """
    def add_historical(self, category, value):
        history = self.historical.get(category, [])
        for i in range(self.race.start_date + len(history), int(self.date) + 1):
            history.append(0)
        history[-1] += value
        self.historical[category] = history

    """ Add a message """
    def add_message(self, source, subject, body, link):
        self.messages.append(Message(source=source, subject=subject, date=self.date, body=body, link=link))

    """ Compute score based on intel """
    def calc_score(self):
        #TODO
        pass

    """ Get the minister for a given planet """
    def get_minister(self, planet):
        for m in self.planetary_ministers:
            if planet in m.planets:
                return m
        for m in self.planetary_ministers:
            if m.new_colony_minister:
                return m
        return self.planetary_ministers[0]
    
    """ Calls the energy mineister to allocate the budget """
    def allocate_budget(self):
        total = self.energy
        for category in ['construction', 'mattrans', 'research']:
            allocation = min(round(total * self['energy_minister_' + category + '_percent'] / 100), self.energy)
            self.__cache__['budget_' + category] = allocation
            self.energy -= allocation

    """ Request to spend energy for a category """
    def spend(self, sub_category, request=sys.maxsize, spend=True):
        category = sub_category
        # Pull from the correct budget category
        if sub_category in ['Ship', 'StarBase', 'Facility', 'baryogenesis']:
            category = 'construction'
            budget = self.__cache__['budget_construction']
        elif category == 'mattrans':
            budget = self.__cache__['budget_mattrans']
            if self.energy_minister_mattrans_use_surplus:
                budget += self.__cache__['budget_construction']
        elif category == 'research':
            budget = self.__cache__['budget_research']
            if self.energy_minister_research_use_surplus:
                budget += self.__cache__['budget_construction']
                budget += self.__cache__['budget_mattrans']
        # All other categories pull from the unallocated budget and surplus
        else:
            category = 'unallocated'
            budget = self.energy
            budget += self.__cache__['budget_construction']
            budget += self.__cache__['budget_mattrans']
            budget += self.__cache__['budget_research']
        # If not enough budget then adjust request
        if request > budget:
            request = budget
        if spend:
            self.add_historical('spend_' + sub_category, request)
            if category == 'unallocated':
                self.energy -= request
            else:
                self.__cache__['budget_' + category] -= request
        # Return approved or adjusted request
        return request

    """ Calls the energy mineister to return unused budget """
    def deallocate_budget(self):
        for category in ['construction', 'mattrans', 'research']:
            self.energy += self.__cache__['budget_' + category]
            self.__cache__['budget_' + category] = 0
    
    """ Research """
    def research(self):
        budget = self.spend('research')
        while budget > 0:
            # Default field
            field = self.research_field
            # Most expensive field for the top item in the queue
            if len(self.research_queue) > 0:
                field = self.research_queue[0].level.most_expensive_field(self.race, self.tech_level, self.research_partial)
                expensive = -1
                for f in TECH_FIELDS:
                    increase = max(0, research_queue[0].level[field] - self.tech_level[field])
                    cost = self.tech_level.cost_for_next_level(f, race, increase) - self.research_partial[f]
                    if cost > expensive:
                        expensive = cost
                        field = f
            # Lowest field
            elif self.research_field == '<LOWEST>':
                lowest = -1
                for f in TECH_FIELDS:
                    if self.tech_level[f] > lowest[1]:
                        lowest = self.tech_level[f]
                        field = f
            # Cost to get to the next level in the selected field
            cost = self.tech_level.cost_for_next_level(field, self.race) - self.research_partial[field]
            # Mad scientist gets 130% return with 55% in the selected field and 15% in every other field
            if self.race.lrt_MadScientist:
                to_each = ceil(cost * 0.15)
                spend = min(cost + to_each * 3, budget)
                to_each = ceil(spend * 0.15) # recalculate to account for budget constraints
                for f in TECH_FIELDS:
                    if f == field:
                        self.research_partial[f] += spend - to_each * 3
                    else:
                        self.research_partial[f] += to_each
            # Spend in the given field
            else:
                spend = min(cost, budget)
                self.research_partial[field] += spend
            # Decrease budget
            budget -= spend
            # Check for tech level-ups
            for f in TECH_FIELDS:
                cost_next = self.tech_level.cost_for_next_level(f, race)
                while self.research_partial[f] > cost_next:
                    self.tech_level[f] += 1
                    self.research_partial[f] -= cost_next
                    cost_next = self.tech_level.cost_for_next_level(f, race)
            # Scrub the research queue
            for t in self.research_queue:
                if t.level.is_available(self.tech_level):
                    self.research_queue.remove(t)


Player.set_defaults(Player, __defaults)
