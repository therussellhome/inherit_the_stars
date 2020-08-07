import unittest
import copy
from .. import *

class NewGameTestCase(unittest.TestCase):
    def test_calc_num_systems(self):
        ng = new_game.NewGame()
        self.assertEqual(ng.calc_num_systems(500, 500, 500, 8), 524)
        self.assertEqual(ng.calc_num_systems(500, 500, 0, 8), 209)
        self.assertEqual(ng.calc_num_systems(500, 50, 0, 8), 21)
        self.assertEqual(ng.calc_num_systems(50, 50, 50, 8), 1)
        self.assertEqual(ng.calc_num_systems(50, 50, 50, 50), 3)
        self.assertEqual(ng.calc_num_systems(25, 25, 100, 50), 2)
        self.assertEqual(ng.calc_num_systems(25, 50, 100, 50), 3)
        self.assertEqual(ng.calc_num_systems(2, 2, 1, 50), 0)

    def test_create_systems(self):
        ng = new_game.NewGame()
        names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.assertLess(len(ng.create_systems(10, copy.copy(names), 5, 5, 5)), 5)
        self.assertEqual(len(ng.create_systems(10, copy.copy(names), 500, 500, 500)), 10)
        self.assertEqual(len(ng.create_systems(20, copy.copy(names), 500, 500, 500)), 10)

    def test_create_systems2(self):
        ng = new_game.NewGame()
        names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.assertEqual(len(ng.create_systems(2, copy.copy(names), 5, 5, 5)), 2, msg='NOTE: this will sometimes fail as it is statistical in nature')

    def test_generate_home_systems(self):
        ng = new_game.NewGame()
        s0 = star_system.StarSystem()
        s1 = star_system.StarSystem()
        s2 = star_system.StarSystem()
        s3 = star_system.StarSystem()
        s4 = star_system.StarSystem()
        s5 = star_system.StarSystem(location=location.Location(x=100, y=50, z=100))
        s6 = star_system.StarSystem(location=location.Location(x=-100, y=-50, z=-100))
        homes = ng.generate_home_systems(2, [s0, s1], 50)
        self.assertIn(s0, homes)
        self.assertIn(s1, homes)
        homes = ng.generate_home_systems(2, [s0, s1, s2, s3, s4, s5], 50)
        self.assertIn(s0, homes)
        self.assertIn(s5, homes)
        homes = ng.generate_home_systems(3, [s0, s1, s2, s3, s4, s5, s6], 50)
        self.assertIn(s0, homes)
        self.assertIn(s5, homes)
        self.assertIn(s6, homes)
