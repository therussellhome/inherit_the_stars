import unittest
from .. import *

class StarsMathTestCase(unittest.TestCase):
    def test_add1(self):
        self.assertEqual(stars_math.volume_add(0, 200), 200)

    def test_add2(self):
        self.assertEqual(stars_math.volume_add(200, 0), 200)

    def test_add3(self):
        self.assertEqual(stars_math.volume_add(100, 200), 208.01)

    def test_vol1(self):
        self.assertAlmostEqual(stars_math.volume(100), 4188790.2047863905)

    def test_distance1(self):
        self.assertEqual(stars_math.distance(0, 0, 0, 1, 0, 0), 1)

    def test_distance2(self):
        self.assertEqual(stars_math.distance(0, 0, 0, 1, 1, 0), 2**.5)
