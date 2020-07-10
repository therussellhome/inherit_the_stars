import unittest
from math import pi
from .. import *

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

    def test_rand(self):
        l0 = location.Location(x=0, y=0, z=0)
        count_gt = 0
        for i in range(0, 100):
            # test if in inner sphere vs outer shell
            if l0 - location.rand_location() > .5 ** (1/3):
                count_gt += 1
        self.assertGreater(count_gt, 40, msg='NOTE: this will sometimes fail as it is statistical in nature')
        self.assertLess(count_gt, 60, msg='NOTE: this will sometimes fail as it is statistical in nature')
