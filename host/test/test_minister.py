import unittest
from .. import *

class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.minister = minister.Minister(name='Test_Minister')

    def test_equalization(self):
        self.minister.power_plants = 30
        self.minister.factories = 50
        self.minister.mines = 260
        self.minister.defenses = 60
        self.assertEqual(self.minister.power_plants, 14)
        self.assertEqual(self.minister.factories, 20)
        self.assertEqual(self.minister.mines, 41)
        self.assertEqual(self.minister.defenses, 25)
        
