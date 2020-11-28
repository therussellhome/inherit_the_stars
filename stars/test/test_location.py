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

    def test_reference(self):
        ref = _TestLocationReference()
        ref.location = location.Location(x=1, y=2, z=3)
        game_engine.register(ref)
        lr = location.LocationReference(reference=ref)
        self.assertEqual(lr.x, 1)
        self.assertEqual(lr.y, 2)
        self.assertEqual(lr.z, 3)
        lr = location.LocationReference(ref)
        self.assertEqual(lr.x, 1)
        self.assertEqual(lr.y, 2)
        self.assertEqual(lr.z, 3)

    def test_rand(self):
        l0 = location.Location(x=0, y=0, z=0)
        count_gt = 0
        for i in range(0, 100):
            # test if in inner sphere vs outer shell
            if l0 - location.rand_location() > .5 ** (1/3):
                count_gt += 1
        self.assertGreater(count_gt, 40, msg='NOTE: this will sometimes fail as it is statistical in nature')
        self.assertLess(count_gt, 60, msg='NOTE: this will sometimes fail as it is statistical in nature')
