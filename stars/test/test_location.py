import unittest
from math import pi
from .. import *

class _TestLocationReference(game_engine.BaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ID = str(id(self))
        self.name = kwargs.get('name', str(id(self)))
        self.location = location.Location()
        game_engine.register(self)

class LocationCase(unittest.TestCase):
    def test_init1(self):
        l = location.Location(1, 2, 3)
        self.assertEqual(l.xyz, (1, 2, 3))

    def test_init2(self):
        l = location.Location(new_random=(999, 999, 999))
        self.assertNotEqual(l.xyz, (0, 0, 0))
        self.assertTrue(-999 <= l.x <= 999)
        self.assertTrue(-999 <= l.y <= 999)
        self.assertTrue(-999 <= l.z <= 999)

    def test_init3(self):
        r = _TestLocationReference()
        l = location.Location(new_orbit=10, offset=1, reference=r)
        self.assertNotEqual(l.x, 0.0)
        self.assertNotEqual(l.y, 0.0)
        self.assertEqual(l.z, 0.0)

    def test_init4(self):
        l1 = location.Location(1, 2, 3)
        l2 = location.Location(l1)
        self.assertEqual(l2.xyz, (1, 2, 3))

    def test_orbit1(self):
        r = _TestLocationReference()
        l = location.Location(orbit_speed=270, offset=1, reference=r)
        self.assertEqual(l.xyz, (1.0, 0.0, 0.0))
        l.orbit()
        self.assertEqual(l.xyz, (0.0, -1.0, 0.0))

    def test_eq1(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=0, y=0, z=0)
        self.assertTrue(l1 == l2)

    def test_eq2(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=0, z=0)
        self.assertFalse(l1 == l2)

    def test_sub1(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=0, z=0)
        self.assertEqual(l1 - l2, 1)

    def test_sub2(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=1, z=0)
        self.assertEqual(l1 - l2, 2**.5)

    def test_sub3(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=1, z=1)
        self.assertEqual(l1 - l2, 3**.5)
        self.assertEqual(l2 - l1, 3**.5)

    def test_move1(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=0, z=0)
        self.assertEqual(l1.move(l1, 0.5), l1)

    def test_move2(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=0, z=0)
        self.assertEqual(l1.move(l2, 0.5).xyz, (0.5, 0, 0))

    def test_move3(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=0, z=0)
        self.assertEqual(l1.move(l2, 1.5).xyz, (1, 0, 0))

    def test_move4(self):
        l1 = location.Location(x=0, y=0, z=0)
        l2 = location.Location(x=1, y=0, z=0)
        self.assertEqual(l1.move(l2, 0.5, True).xyz, (-0.5, 0, 0))

    def test_move5(self):
        l1 = location.Location(x=5, y=0, z=0)
        l2 = location.Location(x=6, y=0, z=0)
        self.assertEqual(l1.move(l2, 0.5).xyz, (5.5, 0, 0))

    def test_move6(self):
        l1 = location.Location(x=1, y=0, z=0)
        l2 = location.Location(x=0, y=0, z=0)
        self.assertEqual(l1.move(l2, 5, standoff=2).xyz, (2, 0, 0))

    def test_xyz1(self):
        l = location.Location(1, 2, 3)
        self.assertEqual(l.xyz, (1, 2, 3))

    def test_xyz2(self):
        l = location.Location(1, 2, 3)
        self.assertEqual(l.x, 1)

    def test_xyz3(self):
        l = location.Location(1, 2, 3)
        self.assertEqual(l.y, 2)

    def test_xyz4(self):
        l = location.Location(1, 2, 3)
        self.assertEqual(l.z, 3)

    def test_offset1(self):
        r = _TestLocationReference()
        l = location.Location(1, 2, 3, reference=r)
        self.assertEqual(l.xyz, (1, 2, 3))
        r.location = location.Location(10, 10, 10)
        self.assertEqual(l.xyz, (11, 12, 13))

    def test_offset2(self):
        r = _TestLocationReference()
        l = location.Location(offset=10, reference=r)
        self.assertLessEqual(abs(l.x), 10)
        self.assertLessEqual(abs(l.y), 10)
        self.assertLessEqual(abs(l.z), 10)
        self.assertAlmostEqual(l - location.Location(), 10)

    def test_in_system1(self):
        l = location.Location()
        self.assertFalse(l.in_system)

    def test_in_system2(self):
        l = location.Location(is_system=True)
        self.assertTrue(l.in_system)

    def test_hash1(self):
        l1 = location.Location(1, 2, 3)
        l2 = location.Location(4, 5, 6)
        l3 = location.Location(1, 2, 3)
        d = {l1: 'l1', l2: 'l2'}
        self.assertEqual(d[l3], 'l1')
