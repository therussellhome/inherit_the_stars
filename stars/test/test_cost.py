import unittest
from .. import *

class CostTestCase(unittest.TestCase):
    def test_add(self):
        c1 = cost.Cost(energy=123, silicon=2)
        c2 = cost.Cost(energy=321, silicon=3)
        c3 = c1 + c2
        self.assertEqual(c3.energy, 444)
        self.assertEqual(c3.silicon, 5)
