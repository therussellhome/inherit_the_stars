import unittest
from .. import *


class CostTestCase(unittest.TestCase):
    def test_eq(self):
        c1 = cost.Cost(energy=123, silicon=2)
        c2 = cost.Cost(energy=321, silicon=3)
        c3 = cost.Cost(energy=321, silicon=3)
        self.assertNotEqual(c1, c2)
        self.assertEqual(c2, c3)

    def test_add(self):
        c1 = cost.Cost(energy=123, silicon=2)
        c2 = cost.Cost(energy=321, silicon=3)
        c3 = c1 + c2
        self.assertEqual(c3.energy, 444)
        self.assertEqual(c3.silicon, 5)

    def test_sub(self):
        c1 = cost.Cost(energy=321, silicon=3)
        c2 = cost.Cost(energy=123, silicon=2)
        c3 = c1 - c2
        self.assertEqual(c3.energy, 198)
        self.assertEqual(c3.silicon, 1)

    def test_mul(self):
        c1 = cost.Cost(energy=123, silicon=2)
        c3 = c1 * 3
        self.assertEqual(c3.energy, 369)
        self.assertEqual(c3.silicon, 6)
