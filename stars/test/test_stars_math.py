import unittest
from .. import *

class StarsMathTestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(stars_math.volume_add(0, 200), 200)
        self.assertEqual(stars_math.volume_add(100, 200), 208.01)
