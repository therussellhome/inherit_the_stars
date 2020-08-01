import sys
from . import game_engine
from .cost import Cost
from .defaults import Defaults
from .energy_minister import EnergyMinister
from .intel import Intel
from .minister import Minister
from .race import Race
from .reference import Reference
from .score import Score
from .tech_level import TechLevel

""" Default values (default, min, max)  """
__defaults = {
    'race': [Race()],
    'intel': [{}], # map of intel objects
    'ministers': [[Minister(name='default')]], # modifiable by the player
    'score': [Score()],
    'tech_level': [TechLevel()],
    'next_tech_cost': [TechLevel()],
    'research_field': [''], # modifiable by the player
    'energy': [0, 0, sys.maxsize],
    'energy_minister': [EnergyMinister()],
    'fleets': [[]]
}

""" A player in a game """
class Player(Defaults):
    """ Initialize """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'Player ' + str(id(self))
    
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
        for planet in game_engine.get('Planet/'):
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
        self.energy_minister.allocate_budget(self.energy)
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
        if not self.race.lrt_generalized_research:
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
