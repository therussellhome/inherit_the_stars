import sys
from . import game_engine
from .defaults import Defaults
from .energy_minister import EnergyMinister
from .intel import Intel
from .planetary_minister import PlanetaryMinister
from .race import Race
from .reference import Reference
from .score import Score
from .tech_level import TechLevel
from .fleet import Fleet

""" Default values (default, min, max)  """
__defaults = {
    'seen_players': [[]],
    'date': [0.0, 0.0, sys.maxsize],
    'load_key': [''], # used to validate the player file
    'race': [Race()],
    'intel': [{}], # map of intel objects indexed by object reference
    'messages': [[]], # list of messages from oldest to newest
    'planetary_ministers': [[PlanetaryMinister(name='New Colony Minister', new_colony_minister=True)]], # list of planetary ministers
    'score': [Score()],
    'tech_level': [TechLevel()],
    'next_tech_cost': [TechLevel()],
    'research_field': [''], # modifiable by the player
    'energy': [0, 0, sys.maxsize],
    'energy_minister': [EnergyMinister()],
    'fleets': [[]],
    'tech': [[]], # tech tree
    'treaties': [{}],
    'pending_treaties': [{}],
}

""" A player in a game """
class Player(Defaults):
    """ Initialize """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            if 'race' in kwargs:
                self.name = self.race.name
            else:
                self.name = 'Player ' + str(id(self))
        game_engine.register(self)
    
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

    """ Add a message """
    def add_message(self, source, subject, body, link):
        self.messages.append(Message(source=source, subject=subject, date=self.date, body=body, link=link))

    """ Compute score based on intel """
    def compute_score(self):
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
    
    """ Calles the energy mineister and tells him to alocat the budget """
    def get_budget(self):
        self.energy_minister.allocate_budget(self.energy)
    
    """ Build/research/other economic funcitions """
    # All non-ship / non-intel parts of take turn
    def manage_economy(self):
        # Collect up last years unused resources before planets generate resources
        self.energy = self.energy_minister.construction_budget 
        self.energy += self.energy_minister.mattrans_budget
        self.energy += self.energy_minister.research_budget
        self.energy += self.energy_minister.unallocated_budget 
        # Get the list of planets
        planets = []
        for planet in game_engine.get('Planet'):
            if planet.player.eq(self):
                planets.append(planet)
        planets.sort(key=lambda x: x.on_planet.people)
        # Population growth, recalculate planet value
        for planet in planets:
            planet.planet_value = planet.calc_planet_value(self.race)
            planet.have_babies()
        # Generate resources
        for planet in planets:
            planet.generate_resources()
        # Allocated energy
        self.get_budget()
        # Existing build queue
        for planet in planets:
            planet.do_construction(False)
        # Add auto build
        for planet in planets:
            planet.do_construction(True)
        # Flip the order
        planets.sort(key=lambda x: x.on_planet.people, reverse=True)
        # Create minerals
        for planet in planets:
            planet.do_baryogenesis()
        # Mat-Trans
        for planet in planets:
            planet.do_mattrans()
        # Research
        self._do_research()

    """ Research """
    def _do_research(self):
        budget = self.energy_minister.check_budget('research', self.energy)
        if not self.race.lrt_MadScientist:
            while budget > 0:
                budget = self._research_in_field(self.research_field, budget)
                if budget > 0:
                    self.research_field = self._calc_next_research_field()
        else:
            # TODO
            print('TODO')
        # TODO unlock tech items?

    """ Apply energy to a specific research field """
    def _research_in_field(self, field, budget):
        field_level = getattr(self.tech_level, field)
        field_cost = getattr(self.next_tech_cost, field)
        request = self.energy_minister.spend_budget('research', field_cost)
        field_cost -= request
        budget -= request
        if field_cost == 0:
            field_level += 1
            field_cost = self._calc_research_cost(field, field_level)
        setattr(self.tech_level, field, field_level)
        setattr(self.next_tech_cost, field, field_cost)
        return budget

    """ Calculate the cost of the next tech level in that field """
    def _calc_research_cost(self, field, level):
        # TODO
        return 100 * level

    """ Determine the next research field """
    def _calc_next_research_field(self):
        # TODO
        return self.research_field


Player.set_defaults(Player, __defaults)
