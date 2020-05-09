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
    minister = Minister(name='Test_Minister')
    minister.power_plants = 30
    minister.factories = 50
    minister.mines = 260
    minister.defenses = 30
    minister.research = 30
    if minister.power_plants != 12: print('minister._test_edit power_plants ', minister.power_plants)
    if minister.factories != 20: print('minister._test_edit factories', minister.factories)
    if minister.mines != 41: print('minister._test_edit mines', minister.mines)
    if minister.defenses != 12: print('minister._test_edit defenses', minister.defenses)
    if minister.research != 15: print('minister._test_edit research', minister.research)
    print('minister._test_edit - end')
