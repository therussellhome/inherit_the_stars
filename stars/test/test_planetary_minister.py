import unittest
from .. import *

class PlanetaryMinisterTestCase(unittest.TestCase):
    def test_equalization(self):
        m = planetary_minister.PlanetaryMinister()
        m.power_plants = 30
        m.factories = 50
        m.mineral_extractors = 260
        m.defenses = 60
        m.normalize()
        self.assertEqual(m.power_plants, 14)
        self.assertEqual(m.factories, 20)
        self.assertEqual(m.mineral_extractors, 41)
        self.assertEqual(m.defenses, 25)
