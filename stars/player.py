import sys
import uuid
from math import ceil
from . import game_engine
from .defaults import Defaults
from .intel import Intel, IntelHistory
from .minister import Minister
from .planetary_minister import PlanetaryMinister
from .race import Race
from .reference import Reference
from .score import Score
from .treaty import Treaty
from .tech_level import TechLevel, TECH_FIELDS
from .fleet import Fleet
from .ship import Ship
from .cargo import Cargo
from .waypoint import Waypoint
from .message import Message
# for testing
from .planet import Planet
from .facility import Facility
from .ship_design import ShipDesign
from .cost import Cost


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
    'planets': [], # list of colonized planets
    'ministers': [],
    'planetary_minister_map': {}, # map of planet references to minister references
    'score': Score(),
    'tech_level': TechLevel(), # current tech levels
    'research_partial': TechLevel(), # energy spent toward next level
    'research_queue': [], # queue of tech items to research
    'ship_designs': [ShipDesign(cost = Cost(energy = 2000, titanium = 50, lithium = 13, silicon = 24))], # the existing designs
    'research_field': '<LOWEST>', # next field to research (or 'lowest')
    'energy': (0, 0, sys.maxsize),
    'fleets': [],
    'tech': [], # tech tree
    'treaties': [],
    'build_queue': [], # array of BuildQueue items
    'finance_construction_percent': (90, 0, 100),
    'finance_mattrans_percent': (0, 0, 100),
    'finance_mattrans_use_surplus': False,
    'finance_research_percent': (10, 0, 100),
    'finance_research_use_surplus': False,
    'finance_baryogenesis_default': True,
    'historical': {}, # map of category to value by year (not hundreth)
}


""" List of fields that are user modifable """
_player_fields = [
    'ready_to_generate',
    'planetary_minister_map',
    'research_queue',
    'research_field',
    'fleets',
    'messages',
    'ministers',
    'ship_designs',
    'treaties',
    'build_queue',
    'finance_construction_percent',
    'finance_mattrans_percent',
    'finance_mattrans_use_surplus',
    'finance_research_percent',
    'finance_research_use_surplus',
]


""" A player in a gaproductionme """
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
        if 'ministers' not in kwargs:
            self.ministers.append(Minister(ID='Admiralty'))
            self.add_message(sender=Reference('Minister/Admiralty'), message='introduction')
            self.ministers.append(Minister(ID='Foreign'))
            self.add_message(sender=Reference('Minister/Foreign'), message='introduction')
            self.ministers.append(Minister(ID='Finance'))
            self.add_message(sender=Reference('Minister/Finance'), message='introduction')
            self.ministers.append(Minister(ID='Research'))
            self.add_message(sender=Reference('Minister/Research'), message='introduction')
            self.ministers.append(PlanetaryMinister(name='Home'))
            self.add_message(sender=Reference(self.ministers[-1]), message='introduction1')
            for planet in self.planets:
                self.planetary_minister_map[Reference(planet)] = Reference(self.ministers[-1])
            self.ministers.append(PlanetaryMinister(name='Colony', new_colony_minister=True))
            self.add_message(sender=Reference(self.ministers[-1]), message='introduction2')
        game_engine.register(self)
        self.__cache__ = {}
        #'''Test line
        if len(self.fleets) < 3:
            fleet_3 = Fleet(
                name = 'Fleet 3', 
                ships = [
                    Ship(
                        ID = 'Test Ship3', 
                        fuel = 400, 
                        fuel_max = 400, 
                        cargo = Cargo(
                            people = 200,
                            silicon = 200,
                            lithium = 200,
                            titanium = 200, 
                            cargo_max = 1000
                        ))])
            self.add_fleet(fleet_3)
            self.create_fleet(
                name = 'Fleet 1', 
                ships = [
                    Ship(
                        ID = 'Test Ship1', 
                        fuel = 100, 
                        fuel_max = 400, 
                        cargo = Cargo(
                            people = 100, 
                            titanium = 900, 
                            cargo_max = 1000
                        )), 
                    Ship(
                        ID = 'Test Ship2', 
                        fuel = 100, 
                        fuel_max = 400, 
                        cargo = Cargo(
                            people = 100, 
                            titanium = 100, 
                            cargo_max = 1000
                        ))],
                waypoints = [
                    Waypoint(),
                    Waypoint(
                        actions = ['load', 'split', 'merge'],
                        #transfers = {'load': [['silicon', 200], ['lithium', 200], ['people', 200], ['titanium', 200], ['fuel': 400]]},
                        splits = [[Reference('Ship/Test Ship2')], [Reference('Ship/Test Ship2')]],
                        #recipiants = {'merge': Reference(self.fleets[0]), 'load': Reference(fleet_3)}
                    )])#'''

    """ Player filename """
    def filename(self):
        return self.game_ID + ' - ' + self.ID

    """ Save player to file """
    def save(self):
        colonized_planets = []
        for planet in game_engine.get('Planet'):
            if planet.is_colonized() and planet.player.ID == self.ID:
                colonized_planets.append(planet)
        self.__colonized_planets = colonized_planets
        game_engine.save('Player', self.filename(), self)
            

    """ Update self from file """
    def update_from_file(self):
        global _player_fields
        p = game_engine.load_inspect('Player', self.filename())
        if self.validation_key == p.validation_key:
            for field in _player_fields:
                self[field] = p[field]
    
    def get_planetary_minister(self, Id, name=False):
        for minister in self.planetary_ministers:
            if minister.name == Id and name:
                return minister
            elif minister.ID == Id and not name:
                return minister
        return self.planetary_ministers[0]
    
    """ Update the date """
    def next_hundreth(self):
        self.date = '{:01.2f}'.format(float(self.date) + 0.01)

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
    
    """ Get the local name for something """
    def get_name(self, obj):
        return self.get_intel(reference=Reference(obj)).name

    """ Store historical values - accumulates across the year """
    def add_historical(self, category, value):
        history = self.historical.get(category, [])
        for i in range(self.race.start_date + len(history), int(self.date) + 1):
            history.append(0)
        history[-1] += value
        self.historical[category] = history

    """ Add a message """
    def add_message(self, **kwargs):
        self.messages.append(Message(**kwargs, date=self.date))

    """ Cleanup messages """
    def cleanup_messages(self):
        for msg in self.messages:
            if msg.star == False and msg.read == True:
                self.messages.remove(msg)
    
    """ Compute score based on intel """
    def calc_score(self):
        #TODO
        pass
    
    """ Get the minister for a given planet """
    def get_minister(self, planet):
        return self.planetary_minister_map.get(Reference(planet), PlanetaryMinister())
    
    """ Share treaty updates with other players """
    def treaty_negotiations(self):
        for t in self.treaties:
            t.other_player.negotiate_treaty(t.for_other_player(self))

    """ Merge in any incoming treaty updates """
    def negotiate_treaty(self, treaty):
        if treaty.status == 'pending':
            self.add_message(sender=Reference('Minister/Foreign'), message='proposed_treaty', parameters=[self.get_name(treaty.other_player)])
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
                self.add_message(sender=Reference('Minister/Foreign'), message='foreign_minister.rejected_treaty', parameters=[self.get_name(t.other_player)])
            elif t.status == 'signed':
                self.add_message(sender=Reference('Minister/Foreign'), message='foreign_minister.accepted_treaty', parameters=[self.get_name(t.other_player)])
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
    
    """ prodict the next years budget """
    def predict_budget(self):
        return 10000
    
    """ Allocate the available energy into budget categories """
    def allocate_budget(self):
        total = self.energy
        for category in ['construction', 'mattrans', 'research']:
            allocation = min(round(total * self['finance_' + category + '_percent'] / 100), self.energy)
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
            if self.finance_mattrans_use_surplus:
                budget += self.__cache__['budget_construction']
        elif category == 'research':
            budget = self.__cache__['budget_research']
            if self.finance_research_use_surplus:
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
                    # Find new available tech
                    for t in self.tech:
                        if t.level[f] == self.tech_level[f] and t.level.is_available(self.tech_level):
                            self.add_message(sender=Reference('Minister/Research'), message='new_tech', parameters=[t.ID], action='show_tech(\'' + t.ID + '\')')
            # Scrub the research queue
            for t in self.research_queue:
                if t.level.is_available(self.tech_level):
                    self.research_queue.remove(t)

                    
Player.set_defaults(Player, __defaults)
