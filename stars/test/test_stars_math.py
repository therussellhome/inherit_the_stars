import unittest
from .. import *

class StarsMathTestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(stars_math.volume_add(0, 200), 200)
        self.assertEqual(stars_math.volume_add(100, 200), 208.01)

    def test_distance(self):
        self.assertEqual(stars_math.distance(0, 0, 0, 1, 0, 0), 1)
        self.assertEqual(stars_math.distance(0, 0, 0, 1, 1, 0), 2**.5)
