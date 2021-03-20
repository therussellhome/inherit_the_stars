import sys
import unittest
from .. import *

class CargoTestCase(unittest.TestCase):
    def test_add(self):
        c1 = cargo.Cargo(people=123, titanium=6, silicon=2, cargo_max=999)
        c2 = cargo.Cargo(people=321, lithium = 9, silicon=3, cargo_max=cargo.sys.maxsize)
        c3 = c1 + c2
        self.assertEqual(c3.people, 444)
        self.assertEqual(c3.titanium, 6)
        self.assertEqual(c3.lithium, 9)
        self.assertEqual(c3.cargo_max, cargo.sys.maxsize)
        self.assertEqual(c3.silicon, 5)

    def test_max1(self):
        c1 = cargo.Cargo(cargo_max=-1)
        self.assertEqual(c1.cargo_max, sys.maxsize)

    def test_percent_full1(self):
        c1 = cargo.Cargo(people=123, titanium=6, silicon=2, cargo_max=524)
        self.assertEqual(c1.percent_full(), 0.25)
