import unittest
from .. import *


class BombTestCase(unittest.TestCase):
    def test_defense(self):
        b = bomb.Bomb(max_defense=115)
        self.assertEqual(b.percent_defense(1000000, 0), 0)
        self.assertGreater(b.percent_defense(1000, 999999999999), 114)
        self.assertGreater(b.percent_defense(1000, 1000), 21)
        self.assertLess(b.percent_defense(1000, 1000), 22)
        b = bomb.Bomb(max_defense=75)
        self.assertGreater(b.percent_defense(1000, 999999999999), 74)

    def test_kill_shields(self):
        b = bomb.Bomb(shield_kill=3)
        self.assertEqual(b.kill_shield_facilities(1000000, 0), 3)
        self.assertEqual(b.kill_shield_facilities(1000000, 999999999999), 0)

    def test_kill_pop(self):
        b = bomb.Bomb(minimum_pop_kill=123)
        self.assertEqual(b.kill_population(1000000, 0), 123)
        b = bomb.Bomb(percent_pop_kill=10)
        self.assertEqual(b.kill_population(1000000, 0), 100000)
        b = bomb.Bomb(percent_pop_kill=10, max_defense=115)
        self.assertEqual(b.kill_population(1000000, 999999999999), 0)
