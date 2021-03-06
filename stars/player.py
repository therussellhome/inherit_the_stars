import sys
import uuid
from math import ceil
from . import game_engine
from .defaults import Defaults
from .intel import Intel, IntelHistory
from .planetary_minister import PlanetaryMinister
from .race import Race
from .reference import Reference
from .score import Score
from .treaty import Treaty
from .tech_level import TechLevel, TECH_FIELDS
from .fleet import Fleet


""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID', # player ID defaulted to a UUID if not provided from the race ID
    'validation_key': '', # used to verify this file against the game file
    'game_ID': '', # name of game for when generating
    'ready_to_generate': False,
    'date': '0.00',
    'race': Race(),
    'computer_player': False,
    'intel': {}, # map of intel objects indexed by object reference
    'messages': [], # list of messages from oldest to newest
    'planetary_ministers': [PlanetaryMinister(name='Planetary Minister', new_colony_minister=True)], # list of planetary ministers
    'planetary_minister_map': {}, # map of planet references to minister references
    'score': Score(),
    'tech_level': TechLevel(), # current tech levels
    'research_partial': TechLevel(), # energy spent toward next level
    'research_queue': [], # queue of tech items to research
    'ship_designs': [], # the existing designs
    'research_field': '<LOWEST>', # next field to research (or 'lowest')
    'energy': (0, 0, sys.maxsize),
    'fleets': [],
    'tech': [], # tech tree
    'treaties': [],
    'build_queue': [], # array of BuildQueue items
    'finance_minister_construction_percent': (90, 0, 100),
    'finance_minister_mattrans_percent': (0, 0, 100),
    'finance_minister_mattrans_use_surplus': False,
    'finance_minister_research_percent': (10, 0, 100),
    'finance_minister_research_use_surplus': False,
    'finance_minister_baryogenesis_default': True,
    'historical': {}, # map of category to value by year (not hundreth)
}


""" List of fields that are user modifable """
_player_fields = [
    'ready_to_generate',
    'planetary_ministers',
    'research_queue',
    'research_field',
    'fleets',
    'ship_designs',
    'treaties',
    'finance_minister_construction_percent',
    'finance_minister_mattrans_percent',
    'finance_minister_mattrans_use_surplus',
    'finance_minister_research_percent',
    'finance_minister_research_use_surplus',
]


""" A player in a game """
class Player(Defaults):
    """ Initialize """
    def __init__(self, **kwargs):
        if 'ID' not in kwargs and 'race' in kwargs and kwargs['race'].ID != '':
            kwargs['ID'] = kwargs['race'].ID
        super().__init__(**kwargs)
        if 'validation_key' not in kwargs:
            self.validation_key = str(uuid.uuid4())
        if 'date' not in kwargs:
            self.date = '{:01.2f}'.format(self.race.start_date)
        game_engine.register(self)
        self.__cache__ = {}

    """ Player filename """
    def filename(self):
        return self.game_ID + ' - ' + self.ID

    """ Save player to file """
    def save(self):
        game_engine.save('Player', self.filename(), self)

    """ Update self from file """
    def update_from_file(self):
        global _player_fields
        p = game_engine.load_inspect('Player', self.filename())
        if self.validation_key == p.validation_key:
            for field in _player_fields:
                self[field] = p[field]

    """ Update the date """
    def next_hundreth(self):
        self.date = '{:01.2f}'.format(float(self.date) + 0.01)

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
        reference = Reference(obj)
        if reference not in self.intel:
            if reference ^ 'Ship' or reference ^ 'Asteroid':
                self.intel[reference] = IntelHistory()
            else:
                self.intel[reference] = Intel()
            self.intel[reference].name = reference.ID
        self.intel[reference].add_report(date=self.date, **kwargs)

    """ Get intel about an object or objects """
    def get_intel(self, reference=None, by_type=None):
        if reference:
            if reference in self.intel:
                return self.intel[reference]
            return None
        elif by_type:
            intel = {}
            for (k, v) in self.intel.items():
                if k ^ by_type:
                    intel[k] = v
            return intel
    
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
    
    """ Share treaty updates with other players """
    def treaty_negotiations(self):
        for t in self.treaties:
            t.other_player.negotiate_treaty(t.for_other_player(self))

    """ Merge in any incoming treaty updates """
    def negotiate_treaty(self, treaty):
        for t in self.treaties:
            if t.treaty_key == treaty.treaty_key and t != treaty:
                t.merge(treaty)
                return
        self.treaties.append(treaty)

    """ Share treaty updates with other players """
    def treaty_finalization(self):
        for t in self.treaties:
            if t.status == 'rejected':
                self.treaties.remove(t)
            elif t.status == 'signed':
                # clear old active treaty (if there was one)
                for t0 in self.treaties:
                    if t.other_player == t0.other_player and t0.status == 'active':
                        self.treaties.remove(t0)
                t.status = 'active'
            
    """ Get the treaty """
    def get_treaty(self, other_player, draft=False):
        other_player = Reference(other_player)
        for t in self.treaties:
            if (t.other_player == other_player) and ((not draft and t.is_active()) or (draft and t.is_draft())):
                return t
        if draft:
            return None
        return Treaty(other_player=other_player, status='active')
    
    """ Allocate the available energy into budget categories """
    def allocate_budget(self):
        total = self.energy
        for category in ['construction', 'mattrans', 'research']:
            allocation = min(round(total * self['finance_minister_' + category + '_percent'] / 100), self.energy)
            self.__cache__['budget_' + category] = allocation

    """ Request to spend energy for a category """
    def spend(self, sub_category, request=sys.maxsize, spend=True):
        category = sub_category
        # Pull from the correct budget category
        if sub_category in ['Ship', 'StarBase', 'Facility', 'baryogenesis']:
            category = 'construction'
            budget = self.__cache__['budget_construction']
        elif category == 'mattrans':
            budget = self.__cache__['budget_mattrans']
            if self.finance_minister_mattrans_use_surplus:
                budget += self.__cache__['budget_construction']
        elif category == 'research':
            budget = self.__cache__['budget_research']
            if self.finance_minister_research_use_surplus:
                budget += self.__cache__['budget_construction']
                budget += self.__cache__['budget_mattrans']
        # All other categories pull from the unallocated budget and surplus
        else:
            category = 'other'
            budget = self.energy
        budget = min(self.energy, budget)
        # If not enough budget then adjust request
        if request > budget:
            request = budget
        if spend:
            self.add_historical('spend_' + sub_category, request)
            self.energy -= request
            if category != 'other':
                self.__cache__['budget_' + category] -= request
        # Return approved or adjusted request
        return request

    """ Attempt to build the items in the build queue """
    def build_from_queue(self):
        for b in self.build_queue:
            if b.planet.build(b):
                self.build_queue.remove(b)

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
                    if self.tech_level[f] > lowest:
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
                cost_next = self.tech_level.cost_for_next_level(f, self.race)
                while self.research_partial[f] >= cost_next:
                    self.tech_level[f] += 1
                    self.research_partial[f] -= cost_next
                    cost_next = self.tech_level.cost_for_next_level(f, self.race)
            # Scrub the research queue
            for t in self.research_queue:
                if t.level.is_available(self.tech_level):
                    self.research_queue.remove(t)

                    
Player.set_defaults(Player, __defaults)
