import unittest
from math import pi
from .. import *

class _TestLocationReference(game_engine.BaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name', str(id(self)))
        self.location = location.Location()

class LocationCase(unittest.TestCase):
    def test_sub(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=0, z=0)
        self.assertEqual(l1 - l2, 1)
        l2 = location.Location(x=1, y=1, z=0)
        self.assertEqual(l1 - l2, 2**.5)
        l2 = location.Location(x=1, y=1, z=1)
        self.assertEqual(l1 - l2, 3**.5)
        self.assertEqual(l2 - l1, 3**.5)

    def test_eq(self):
        l0 = location.Location(x=0, y=0, z=0)
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=0, z=0)
        self.assertTrue(l0 == l1)
        self.assertFalse(l1 == l2)

    def test_move(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=0, z=0)
        l3 = l1.move(l1, 0.5)
        self.assertEqual(l3, l1)
        l3 = l1.move(l2, 0.5)
        self.assertEqual(l3.x, 0.5)
        self.assertEqual(l3.y, 0)
        self.assertEqual(l3.z, 0)
        l3 = l1.move(l2, 1.5)
        self.assertEqual(l3.x, 1)
        self.assertEqual(l3.y, 0)
        self.assertEqual(l3.z, 0)
        l3 = l1.move(l2, 0.5, True)
        self.assertEqual(l3.x, -0.5)
        self.assertEqual(l3.y, 0)
        self.assertEqual(l3.z, 0)
        l1 = location.Location(x=5, y=0, z=0)
        l2 = location.Location(x=6, y=0, z=0)
        l3 = l1.move(l2, 0.5)
        self.assertEqual(l3.x, 5.5)
        self.assertEqual(l3.y, 0)
        self.assertEqual(l3.z, 0)
