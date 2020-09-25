import unittest
from .. import *

class PlanetaryMinisterTestCase(unittest.TestCase):
    def test_equalization(self):
        m = planetary_minister.PlanetaryMinister()
        m.power_plants = 30
        m.factories = 50
        m.mines = 260
        m.defenses = 60
        self.assertEqual(m.power_plants, 14)
        self.assertEqual(m.factories, 20)
        self.assertEqual(m.mines, 41)
        self.assertEqual(m.defenses, 25)
