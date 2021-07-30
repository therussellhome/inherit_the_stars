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
