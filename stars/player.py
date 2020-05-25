import sys
from . import game_engine
from .cost import Cost
from .defaults import Defaults
from .minister import Minister
from .race import Race
from .reference import Reference
from .score import Score
from .tech_level import TechLevel
from .energy_minister import EnergyMinister

""" Default values (default, min, max)  """
__defaults = {
    'race': [Race()],
    'ministers': [[Minister(name='default')]],
    'score': [Score()],
    'tech_level': [TechLevel()],
    'next_tech_cost': [TechLevel()],
    'research_field': [''],
    'energy': [0, 0, sys.maxsize],
    'energy_minister': [EnergyMinister()],
}

""" A player in a game """
class Player(Defaults):
    """ Initialize """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'Player_' + str(id(self))
        game_engine.register(self)
    
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
        # Population growth
        for planet in planets:
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
        self.do_research()

    """ Research """
    def do_research(self):
        while True:
            if not self.race.generalized_research:
                field_cost = self.next_tech_cost[self.research_field]
                request = self.spend_budget('research', field_cost)
                if request < field_cost:
                    self.next_tech_cost[self.research_field] -= request
                    break
                else:
                    self.tech_level[self.research_field] += 1
                    self.next_tech_cost[self.research_field] = self._calc_research_cost(self.research_field, self.tech_level[self.research_field] + 1)
                    self.research_field = self._calc_next_research_field()
            else:
                print('TODO')
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
