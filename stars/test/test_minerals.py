import unittest
from .. import *


class MineralsTestCase(unittest.TestCase):
    def test_add(self):
        m1 = minerals.Minerals(titanium=1, lithium=2, silicon=3)
        m2 = minerals.Minerals(titanium=3, lithium=2, silicon=1)
        m3 = m1 + m2
        self.assertEqual(m3.titanium, 4)
        self.assertEqual(m3.lithium, 4)
        self.assertEqual(m3.silicon, 4)
