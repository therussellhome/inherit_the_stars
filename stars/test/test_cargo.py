import sys
import unittest
from .. import *

class CargoTestCase(unittest.TestCase):
    def test_add(self):
        c1 = cargo.Cargo(people=123, titanium=6, silicon=2)
        c2 = cargo.Cargo(people=321, lithium = 9, silicon=3)
        c3 = c1 + c2
        self.assertEqual(c3.people, 444)
        self.assertEqual(c3.titanium, 6)
        self.assertEqual(c3.lithium, 9)
        self.assertEqual(c3.silicon, 5)

    def test_sum(self):
        c1 = cargo.Cargo(people=123, titanium=6, silicon=2)
        self.assertEqual(c1.sum(), 131)
