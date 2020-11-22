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
        tech_item = tech_level.TechLevel(evergy=1, weapons=2, propulsion=3, construction=4, electonics=5, biotechnology=6)
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
        self.assertTrue(tech_item.is_available(player_level))
        player_level.energy = 2
        self.assertTrue(tech_item.is_available(player_level))
