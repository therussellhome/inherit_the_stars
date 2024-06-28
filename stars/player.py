import sys
import uuid
from math import ceil
from . import game_engine
from .build_ship import BuildShip
from .cargo import Cargo
from .defaults import Defaults
from .fleet import Fleet
from .intel import Intel
from .message import Message
from .minister import Minister
from .planetary_minister import PlanetaryMinister
from .race import Race
from .reference import Reference
from .treaty import Treaty
from .tech_level import TechLevel, TECH_FIELDS
from .minerals import Minerals, MINERAL_TYPES
from .facility import Facility, FACILITY_TYPES
from .order import Order
from .ship import Ship
from .buships import BuShips

""" Default values (default, min, max)  """
__defaults = {
    'ID': '@UUID', # player ID defaulted to a UUID if not provided from the race ID
    'validation_key': '', # used to verify this file against the game file
    'game': Reference('Game'),
    'game_ID': '', # name of game for when generating
    'ready_to_generate': False,
    'date': '0.00',
    'race': Race(),
    'computer_player': False,
    'intel': {}, # map of intel objects indexed by object reference
    'messages': [], # list of messages from oldest to newest
    'planets': [], # list of colonized planets only updated during save
    'ministers': [],
    'planetary_minister_map': {}, # map of planet references to minister references
    'tech_level': TechLevel(), # current tech levels
    'research_partial': TechLevel(), # energy spent toward next level
    'research_queue': [], # queue of tech items to research
    'ship_designs': [], # the existing designs
    'research_field': '<LOWEST>', # next field to research (or 'lowest')
    'energy': (0, 0, sys.maxsize),
    'fleets': [],
    'ships': [],
    'tech': [], # tech tree
    'treaties': [],
    'build_queue': [], # array of BuildQueue items
    'buships': [], # user modifable queue of ships to build in priority order
    'finance_construction_percent': (90.0, 0.0, 100.0),
    'finance_mattrans_percent': (0.0, 0.0, 100.0),
    'finance_mattrans_use_surplus': False,
    'finance_research_percent': (10.0, 0.0, 100.0),
    'finance_research_use_surplus': False,
    'finance_baryogenesis_default': True,
    'colonize_min_hab': (50, -100, 100),
    'colonize_min_ti': (0, 0, 100),
    'colonize_min_li': (0, 0, 100),
    'colonize_min_si': (0, 0, 100),
}

""" Temporary values (default, min, max)  """
__tmp_defaults = {
    'msg_cache': [],
    'planet_report': [],
    'design_cache': [],
    'budget_construction': 0,
    'budget_mattrans': 0,
    'budget_research': 0,
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
    'buships',
    'finance_construction_percent',
    'finance_mattrans_percent',
    'finance_mattrans_use_surplus',
    'finance_research_percent',
    'finance_research_use_surplus',
    'colonize_min_hab',
    'colonize_min_ti',
    'colonize_min_li',
    'colonize_min_si',
]


""" A player in a game """
class Player(Defaults):
    """ Initialize """
    def __init__(self, *args, **kwargs):
        if 'ID' not in kwargs and 'race' in kwargs and kwargs['race'].ID != '':
            kwargs['ID'] = kwargs['race'].ID
        super().__init__(*args, **kwargs)
        if 'validation_key' not in kwargs:
            self.validation_key = str(uuid.uuid4())
            if len(self.planets) > 0:
                self.planets[0].colonize(self)
                self.planets[0].on_surface.people = self.race.starting_colonists / self.race.pop_per_kt()
                for mineral in MINERAL_TYPES:
                    self.planets[0].on_surface[mineral] = self.race['starting_' + mineral]
                for f in FACILITY_TYPES:
                    self.planets[0][f] = self.race['starting_' + f]
            self.energy = self.race.starting_energy
            for field in TECH_FIELDS: 
                self.tech_level[field] = self.race['starting_tech_' + field]
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
            self.ministers.append(PlanetaryMinister(name='Home', color=self.race.icon_color))
            self.add_message(sender=Reference(self.ministers[-1]), message='introduction1')
            for planet in self.planets:
                self.planetary_minister_map[Reference(planet)] = Reference(self.ministers[-1])
            self.ministers.append(PlanetaryMinister(name='Colony', new_colony_minister=True))
            self.add_message(sender=Reference(self.ministers[-1]), message='introduction2')
        game_engine.register(self)
        for fleet in self.fleets:
            for ship in fleet.ships:
                if Reference(ship) not in self.get_intel(None, 'Ship'):
                    self.add_intel(ship, ship.scan_report())

    def __str__(self):
        return str(self.ID)

    """ Player filename """
    def filename(self):
        return self.game_ID + ' - ' + self.ID

    """ Save player to file """
    def save(self):
        colonized_planets = []
        for planet in game_engine.get('Planet'):
            if planet.is_colonized() and planet.player.ID == self.ID:
                colonized_planets.append(planet)
        self.planets = colonized_planets
        game_engine.save('Player', self.filename(), self)
            

    """ Update self from file """
    def update_from_file(self):
        global _player_fields
        p = game_engine.load_inspect('Player', self.filename())
        if self.validation_key == p.validation_key:
            for field in _player_fields:
                self[field] = p[field]
                print(field, p[field])
      
    """ Get the minister for a given planet """
    def get_minister(self, planet):
        planet_ref = Reference(planet)
        if planet_ref in self.planetary_minister_map:
            return self.planetary_minister_map[Reference(planet)]
        else:
            for minister in self.ministers:
                if hasattr(minister, 'new_colony_minister'):
                    if minister.new_colony_minister:
                        return minister
        minister = PlanetaryMinister(name='Colony', new_colony_minister=True)
        self.ministers.append(minister)
        return minister

    """ Reconcile fleets """
    def reconcile_fleets(self):
        for f in self.fleets:
            f.player = Reference(self)
        #TODO cheating check for multiple fleets pointing to the same ship

    """ Apply the buships plan """
    def reconcile_buships(self):
        # link all buships and remove from build queue
        for build_ship in self.build_queue:
            if isinstance(build_ship, BuildShip):
                if build_ship.buships:
                    build_ship.buships.queue(build_ship)
                self.build_queue.remove(build_ship)
        # add all the buships back at the front of the queue
        for buship in reversed(self.buships):
            self.build_queue.insert(0, buship.queue())

    """ Update the date """
    def next_hundreth(self):
        self.date = '{:01.2f}'.format(float(self.date) + 0.01)

    """ Update stats """
    def update_stats(self):
        minerals = 0
        unarmed = 0
        escort = 0
        wall = 0
        starbases = 0
        score = 0
        for f in self.fleets:
            for s in f.ships:
                minerals += s.cargo.titanium + s.cargo.lithium + s.cargo.silicon
                if s.is_space_station():
                    starbases += 1
                elif len(s.weapons) == 0:
                    unarmed += 1
                elif len(s.weapons) < 10: #TODO what decides escort vs wall?
                    escort += 1
                else:
                    wall += 1
        for p in self.planets:
            minerals += p.on_surface.titanium + p.on_surface.lithium + p.on_surface.silicon
        self.add_intel(self, 
                {'planets': len(self.planets),
                'energy': self.energy,
                'tech_levels': self.tech_level.total_levels(),
                'minerals': minerals,
                'ships_unarmed': unarmed,
                'ships_escort': escort,
                'ships_of_the_wall': wall,
                'starbases': starbases,
                'score': score,})
        #TODO calculate score

    """ Add ships to the player and put them in a new fleet """
    def add_ships(self, ships, fleet=None):
        if not isinstance(ships, list):
            ships = [ships]
        if not fleet:
            if isinstance(ships[0], BuShips) or (isinstance(ships[0], Reference) and ships[0] ^ 'BuShips'):
                location = ships[0].ship.location
            else:
                location = ships[0].location
            fleet = Fleet(player=Reference(self), order=Order(location=location))
            self.fleets.append(fleet)
        for s in ships:
            if isinstance(s, Reference):
                s = ~s
            if isinstance(s, Ship): # Don't add unbuilt ships to the ship list
                self.ships.append(s)
            fleet + Reference(s)
        return Reference(fleet)
    
    """ Remove a fleet and any ships it had """
    def remove_ships(self, ships=[]):
        if isinstance(ships, Fleet):
            if ships in self.fleets:
                self.fleets.remove(ships)
            ships = ships.ships
        elif isinstance(ships, Reference) and ships ^ 'Fleet':
            if ~ships in self.fleets:
                self.fleets.remove(~ships)
            ships = ships.ships
        elif not isinstance(ships, list):
            ships = [ships]
        for s in ships:
            if isinstance(s, Reference):
                s = ~s
            if s in self.ships:
                self.ships.remove(s)
            for f in self.fleets:
                if s in f.ships:
                    f.ships.remove(s)
    
    """ Return the id for use as a temporary player token """
    def token(self):
        return str(id(self))

    """ Add an intel report """
    def add_intel(self, obj, report):
        reference = Reference(obj)
        if reference not in self.intel:
            self.intel[reference] = Intel(name=reference.ID)
        self.intel[reference].add_report(reference, self.date, report)

    """ Get intel about an object or objects """
    def get_intel(self, reference=None, by_type=None):
        if reference:
            reference = Reference(reference)
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
        intel = self.get_intel(reference=obj)
        if intel:
            return intel.name
        return obj.ID

    """ Add a message """
    def add_message(self, **kwargs):
        self.messages.append(Message(**kwargs, date=self.date))

    """ Cleanup messages """
    def cleanup_messages(self):
        self.messages[:] = [msg for msg in self.messages if msg.star == True or msg.read == False]
    
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
        if other_player is self:
            if draft:
                return None
            return Treaty(other_player = self,
                            relation = 'me',
                            status = 'active',
                            buy_ti = 0,
                            sell_ti = 0,
                            buy_si = 0,
                            sell_si = 0,
                            buy_li = 0,
                            sell_li = 0,
                            buy_fuel = 0,
                            sell_fuel = 0,
                            buy_gate = 0,
                            sell_gate = 0,
                            buy_hyper_denial = 0,
                            sell_hyper_denial = 0,
                            buy_intel = 0,
                            sell_intel = 0)
        other_player = Reference(other_player)
        for t in self.treaties:
            if (t.other_player == other_player) and ((not draft and t.is_active()) or (draft and t.is_draft())):
                return t
        if draft:
            return None
        return Treaty(other_player=other_player, status='active')

    """ Get the relationship """
    def get_relation(self, player):
        if Reference(player) == Reference(self):
            return 'me'
        return self.get_treaty(player).relation

    """ Get max terraform """
    def max_terraform(self):
        if self.race.lrt_Bioengineer == True:
            return min(40, self.tech_level.biotechnology)
        return min(40, self.tech_level.biotechnology) / 2

    """ predict the next 100th's energy income """
    def predict_income(self, category):
        income = 10000 #TODO
        if hasattr(self, 'finance_' + category + '_percent'):
            percent = self['finance_' + category + '_percent']
        else:
            percent = 100 - self['finance_construction_percent'] - self['finance_mattrans_percent'] - self['finance_research_percent']
        return round(income * percent / 100)
    
    """ Allocate the available energy into budget categories """
    def allocate_budget(self):
        allocated = 0
        for category in ['construction', 'mattrans', 'research']:
            allocation = min(allocated + round(self.energy * self['finance_' + category + '_percent'] / 100), self.energy) - allocated
            self['budget_' + category] = allocation
            allocated += allocation

    """ Incoming energy """
    def add_energy(self, energy):
        self.add_intel(self, {'Finance Minister: Income': energy})
        self.energy += energy

    """ Request to spend energy for a category """
    def spend(self, sub_category, request=sys.maxsize, spend=True):
        category = sub_category
        # Pull from the correct budget category
        if sub_category in ['Ship', 'StarBase', 'Facility', 'Baryogenesis']:
            category = 'construction'
            intel_category = 'Finance Minister: ' + sub_category
            budget = self.budget_construction
        elif category == 'mattrans':
            intel_category = 'Finance Minister: MatTrans'
            budget = self.budget_mattrans
            if self.finance_mattrans_use_surplus:
                budget += self.budget_construction
        elif category == 'research':
            intel_category = 'Finance Minister: Research'
            budget = self.budget_research
            if self.finance_research_use_surplus:
                budget += self.budget_construction
                budget += self.budget_mattrans
        # All other categories pull from the unallocated budget and surplus
        else:
            category = 'other'
            intel_category = 'Finance Minister: Other'
            budget = self.energy
        budget = min(self.energy, budget)
        # If not enough budget then adjust request
        if request > budget:
            request = budget
        if spend:
            self.add_intel(self, {intel_category: request})
            self.energy -= request
            if category != 'other':
                self['budget_' + category] -= request
        # Return approved or adjusted request
        return request

    """ Attempt to build the items in the build queues """
    def build_from_queue(self):
        remove_from_queue = []
        for b in self.build_queue:
            if b.planet.player == Reference(self):
                if b.planet.build(b):
                    remove_from_queue.append(b)
            else:
                remove_from_queue.append(b)
        for d in remove_from_queue:
            self.build_queue.remove(d)
            if isinstance(d, BuildShip):
                if d.buships:
                    self.buships.remove(~d.buships)
                    for f in self.fleets:
                        if d.buships in f.under_construction:
                            f - Reference(d.buships)

    """ Research """
    def research(self):
        budget = self.spend('research')
        while budget > 0:
            # Default field
            field = self.research_field
            # Most expensive field for the top item in the queue
            if len(self.research_queue) > 0:
                #field = self.research_queue[0].level.most_expensive_field(self.race, self.tech_level, self.research_partial)
                expensive = -1
                for f in TECH_FIELDS:
                    increase = max(0, self.research_queue[0].level[f] - self.tech_level[f])
                    cost = self.tech_level.cost_for_next_level(f, self.race, increase) - self.research_partial[f]
                    if cost > expensive:
                        expensive = cost
                        field = f
            # Lowest field
            elif self.research_field == '<LOWEST>':
                lowest = sys.maxsize
                for f in TECH_FIELDS:
                    if self.tech_level[f] < lowest:
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

    """ Update ship designs to account for miniaturization """
    def design_miniaturization(self):
        for d in self.ship_designs:
            d.update(miniaturize_level=self.tech_level)

                    
Player.set_defaults(Player, __defaults, __tmp_defaults)
