import unittest
from .. import *

class PlayerTestCase(unittest.TestCase):
    def test_do_research(self):
        #TODO
        return
        p = player.Player()
        p.energy = 1000000
        p.energy_minister.allocate_budget(p.energy)
        p.energy_minister.research_budget = 100
        p.research_field = 'energy'
        p.tech_level.energy = 0
        p.next_tech_cost.energy = 100
        p._do_research()
        self.assertEqual(p.tech_level.energy, 1)
        self.assertEqual(p.energy_minister.research_budget, 0)
        p.energy_minister.research_budget = 300
        p.research_field = 'energy'
        p.tech_level.energy = 0
        p.next_tech_cost.energy = 100
        p._do_research()
        self.assertEqual(p.tech_level.energy, 2)
        self.assertEqual(p.energy_minister.research_budget, 0)

    def test_calc_research_cost(self):
        # TODO
        pass

    def test_calc_next_research_field(self):
        # TODO
        pass
