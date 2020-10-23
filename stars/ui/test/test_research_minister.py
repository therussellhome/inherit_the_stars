import unittest
import copy

class ResearchMinisterTestCase(unittest.TestCase):
    def test_calc_cost(self):
        p = player.Player()
        p.r = race.Race()
        p.r.research_modifier_energy = 75
        p.energy_tech_level = 3
        self.assertEqual(self.p.calc_cost('energy'), 27)
        p.r.research_modifier_weapons = 50
        p.weapons_tech_level = 5
        self.assertEqual(self.p.calc_cost('weapons'), 575)
        p.r.research_modifier_propulsion = 125
        p.propulsion_tech_level = 2
        self.assertEqual(self.p.calc_cost('propulsion'), 268)
        p.r.research_modifier_construction = 100
        p.construction_tech_level = 5
        self.assertEqual(self.p.calc_cost('construction'), 1150)
        p.r.research_modifier_electronics = 150
        p.electronics_tech_level = 4
        self.assertEqual(self.p.calc_cost('electronics'), 993)
        p.r.research_modifier_biotechnology = 200
        p.biotechnology_tech_level = 1
        self.assertEqual(self.p.calc_cost('biotechnology'), 316)
        p.energy_tech_level = 4
        self.assertEqual(self.p.calc_cost('energy'), 497)
        p.weapons_tech_level = 6
        self.assertEqual(self.p.calc_cost('weapons'), 939)
        p.propulsion_tech_level = 3
        self.assertEqual(self.p.calc_cost('propulsion'), 458)
        p.construction_tech_level = 6
        self.assertEqual(self.p.calc_cost('construction'), 1878)
        p.biotechnology_tech_level = 2
        self.assertEqual(self.p.calc_cost('biotechnology'), 428)
    def test_bombs(self):
        pass
    def test_cloaks_and_ecm(self):
        pass
    def test_defense(self):
        pass
    def test_depot(self):
        pass
    def test_engines(self):
        pass
    def test_hulls(self):
        pass
    def test_mech(self):
        pass 
    def test_orbital(self):
        pass
    def test_planetary(self):
        pass
    def test_scanners(self):
        pass
    def test_weapons(self):
        pass
      
