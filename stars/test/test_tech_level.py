import unittest
from .. import *


class TechLevelTestCase(unittest.TestCase):
    def test_add(self):
        t1 = tech_level.TechLevel(energy=1, weapons=2, propulsion=3, construction=4, electronics=5, biotechnology=6)
        t2 = tech_level.TechLevel(energy=6, weapons=5, propulsion=4, construction=3, electronics=2, biotechnology=1)
        t3 = t1 + t2
        self.assertEqual(t3.energy, 6)
        self.assertEqual(t3.weapons, 5)
        self.assertEqual(t3.propulsion, 4)
        self.assertEqual(t3.construction, 4)
        self.assertEqual(t3.electronics, 5)
        self.assertEqual(t3.biotechnology, 6)

    def test_is_available(self):
        tech_item = tech_level.TechLevel(energy=1, weapons=2, propulsion=3, construction=4, electronics=5, biotechnology=6)
        player_level = tech_level.TechLevel(evergy=1)
        self.assertFalse(tech_item.is_available(player_level))
        player_level.weapons = 2
        self.assertFalse(tech_item.is_available(player_level))
        player_level.propulsion = 3
        self.assertFalse(tech_item.is_available(player_level))
        player_level.construction = 4
        self.assertFalse(tech_item.is_available(player_level))
        player_level.electronics = 5
        self.assertFalse(tech_item.is_available(player_level))
        player_level.biotechnology = 6
        self.assertFalse(tech_item.is_available(player_level))
        player_level.energy = 2
        self.assertTrue(tech_item.is_available(player_level))

    def test_cost_next1(self):
        l = tech_level.TechLevel()
        r = race.Race()
        self.assertEqual(l.cost_for_next_level('energy', r), 5500)

    def test_cost_next2(self):
        l = tech_level.TechLevel()
        r = race.Race()
        self.assertEqual(l.cost_for_next_level('energy', r, increase=2), 14500)

    def test_cost1(self):
        l = tech_level.TechLevel()
        t = tech_level.TechLevel(energy=2)
        p = tech_level.TechLevel()
        r = race.Race()
        self.assertEqual(t.calc_cost(r, l, p), 14500)

    def test_cost2(self):
        l = tech_level.TechLevel(energy=1)
        t = tech_level.TechLevel(energy=2)
        p = tech_level.TechLevel()
        r = race.Race()
        self.assertEqual(t.calc_cost(r, l, p), 9000)

    def test_cost3(self):
        l = tech_level.TechLevel()
        t = tech_level.TechLevel(energy=2)
        p = tech_level.TechLevel(energy=500)
        r = race.Race()
        self.assertEqual(t.calc_cost(r, l, p), 14000)

    def test_total1(self):
        l = tech_level.TechLevel(energy=1, weapons=2, propulsion=3, construction=4, electronics=5, biotechnology=6)
        self.assertEqual(l.total_levels(), 21)

    def test_html(self):
        l = tech_level.TechLevel()
        self.assertEqual(l.to_html(show_zero=True), '<i class="fa-react" title="Energy"> 0</i><i class="fa-bomb" title="Weapons"> 0</i><i class="fa-tachometer-alt" title="Propulsion"> 0</i><i class="fa-wrench" title="Construction"> 0</i><i class="fa-plug" title="Electronics"> 0</i><i class="fa-seedling" title="Biotechnology"> 0</i>')
