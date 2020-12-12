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

    def test_allocate(self):
        return # TODO these tests predate the move to player
        m = energy_minister.EnergyMinister()
        # test 1
        m.energy_minister_construction_percent = 100
        m.energy_minister_mattrans_percent = 100
        m.energy_minister_research_percent = 100
        m.allocate_budget(100)
        self.assertEqual(m.construction_budget, 100)
        self.assertEqual(m.mattrans_budget, 0)
        self.assertEqual(m.research_budget, 0)
        self.assertEqual(m.unallocated_budget, 0)
        # test 2
        m.energy_minister_construction_percent = 0
        m.energy_minister_mattrans_percent = 100
        m.energy_minister_research_percent = 100
        m.allocate_budget(100)
        self.assertEqual(m.construction_budget, 0)
        self.assertEqual(m.mattrans_budget, 100)
        self.assertEqual(m.research_budget, 0)
        self.assertEqual(m.unallocated_budget, 0)
        # test 3
        m.energy_minister_construction_percent = 0
        m.energy_minister_mattrans_percent = 0
        m.energy_minister_research_percent = 100
        m.allocate_budget(100)
        self.assertEqual(m.construction_budget, 0)
        self.assertEqual(m.mattrans_budget, 0)
        self.assertEqual(m.research_budget, 100)
        self.assertEqual(m.unallocated_budget, 0)
        # test 4
        m.energy_minister_construction_percent = 0
        m.energy_minister_mattrans_percent = 0
        m.energy_minister_research_percent = 0
        m.allocate_budget(100)
        self.assertEqual(m.construction_budget, 0)
        self.assertEqual(m.mattrans_budget, 0)
        self.assertEqual(m.research_budget, 0)
        self.assertEqual(m.unallocated_budget, 100)
        # test 5
        m.energy_minister_construction_percent = 10
        m.energy_minister_mattrans_percent = 10
        m.energy_minister_research_percent = 10
        m.allocate_budget(100)
        self.assertEqual(m.construction_budget, 10)
        self.assertEqual(m.mattrans_budget, 10)
        self.assertEqual(m.research_budget, 10)
        self.assertEqual(m.unallocated_budget, 70)

    def test_check_budget(self):
        return # TODO these tests predate the move to player
        m = energy_minister.EnergyMinister()
        m.energy_minister_construction_percent = 40
        m.energy_minister_mattrans_percent = 30
        m.energy_minister_research_percent = 20
        m.allocate_budget(100)
        self.assertEqual(m.check_budget('ship', 30), 30)
        self.assertEqual(m.check_budget('ship', 40), 40)
        self.assertEqual(m.check_budget('ship', 111), 40)
        self.assertEqual(m.check_budget('planetary', 111), 40)
        self.assertEqual(m.check_budget('baryogenesis', 111), 40)
        self.assertEqual(m.check_budget('mattrans', 111), 30)
        self.assertEqual(m.check_budget('research', 111), 20)
        self.assertEqual(m.check_budget('trade', 111), 100)
        m.energy_minister_mattrans_use_surplus = True
        self.assertEqual(m.check_budget('mattrans', 111), 70)
        m.energy_minister_research_use_surplus = True
        self.assertEqual(m.check_budget('research', 111), 90)
        self.assertEqual(m.construction_budget, 40)
        self.assertEqual(m.mattrans_budget, 30)
        self.assertEqual(m.research_budget, 20)
        self.assertEqual(m.unallocated_budget, 10)

    def test_spend_budget(self):
        return # TODO these tests predate the move to player
        m = energy_minister.EnergyMinister()
        m.energy_minister_construction_percent = 40
        m.energy_minister_mattrans_percent = 30
        m.energy_minister_research_percent = 20
        m.allocate_budget(100)
        # Construction
        self.assertEqual(m.spend_budget('ship', 1), 1)
        self.assertEqual(m.construction_budget, 39)
        self.assertEqual(m.spend_budget('planetary', 1), 1)
        self.assertEqual(m.construction_budget, 38)
        self.assertEqual(m.spend_budget('baryogenesis', 1), 1)
        self.assertEqual(m.construction_budget, 37)
        # Mattrans
        self.assertEqual(m.spend_budget('mattrans', 111), 30)
        self.assertEqual(m.mattrans_budget, 0)
        m.energy_minister_mattrans_use_surplus = True
        self.assertEqual(m.spend_budget('mattrans', 5), 5)
        self.assertEqual(m.mattrans_budget, -5)
        # Research
        self.assertEqual(m.spend_budget('research', 111), 20)
        self.assertEqual(m.research_budget, 0)
        m.energy_minister_research_use_surplus = True
        self.assertEqual(m.spend_budget('research', 111), 32)
        self.assertEqual(m.research_budget, -32)
        # Unallocated
        self.assertEqual(m.spend_budget('trade', 111), 10)
        self.assertEqual(m.unallocated_budget, 0)
