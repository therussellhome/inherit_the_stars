import unittest
from .. import *

class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.minister = Minister(name='Test_Minister')

    def test_edit():
        self.minister.power_plants = 30
        self.minister.factories = 50
        self.minister.mines = 260
        self.minister.defenses = 30
        self.minister.research = 30
        self.assertEqual(self.minister.power_plants, 12)
        self.assertEqual(self.minister.factories, 20)
        self.assertEqual(self.minister.mines, 41)
        self.assertEqual(self.minister.defenses, 12)
        self.assertEqual(self.minister.research, 15)
