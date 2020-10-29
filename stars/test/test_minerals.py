import unittest
from .. import *


class MineralsTestCase(unittest.TestCase):
    def test_eq(self):
        m1 = minerals.Minerals(titanium=1, lithium=2, silicon=3)
        m2 = minerals.Minerals(titanium=3, lithium=2, silicon=1)
        m3 = minerals.Minerals(titanium=3, lithium=2, silicon=1)
        self.assertNotEqual(m1, m2)
        self.assertEqual(m2, m3)

    def test_add(self):
        m1 = minerals.Minerals(titanium=1, lithium=2, silicon=3)
        m2 = minerals.Minerals(titanium=3, lithium=2, silicon=1)
        m3 = m1 + m2
        self.assertEqual(m3.titanium, 4)
        self.assertEqual(m3.lithium, 4)
        self.assertEqual(m3.silicon, 4)

    def test_sub(self):
        m1 = minerals.Minerals(titanium=5, lithium=4, silicon=3)
        m2 = minerals.Minerals(titanium=3, lithium=2, silicon=1)
        m3 = m1 - m2
        self.assertEqual(m3.titanium, 2)
        self.assertEqual(m3.lithium, 2)
        self.assertEqual(m3.silicon, 2)

    def test_mul(self):
        m1 = minerals.Minerals(titanium=1, lithium=2, silicon=3)
        m3 = m1 * 3
        self.assertEqual(m3.titanium, 3)
        self.assertEqual(m3.lithium, 6)
        self.assertEqual(m3.silicon, 9)
