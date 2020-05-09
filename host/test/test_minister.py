import unittest
from .. import *

class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.minister = Minister(name='Test_Minister')

    def test_edit():
        minister.edit(power_plants=30, factories=50, mines=200, defences=30, research=30)
        if round(minister.power_plants, 1) != 12.5 or round(minister.factories, 1) != 20.8 or round(minister.mines, 1) != 41.7 or round(minister.defences, 1) != 12.5 or round(minister.research, 1) != 12.5:
            print('edit fail', round(minister.power_plants, 1), round(minister.factories, 1), round(minister.mines, 1), round(minister.defences, 1), round(minister.research, 1))
            print('edit fail', minister.power_plants, minister.factories, minister.mines, minister.defences, minister.research)
