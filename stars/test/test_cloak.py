import unittest
from .. import *


class CloakTestCase(unittest.TestCase):
    def test_cloak_add(self):
        c1 = cloak.Cloak(percent=50)
        c2 = cloak.Cloak(percent=50)
        c3 = c1 + c2
        self.assertEqual(c3.percent, 75)
        c1 = cloak.Cloak(percent=0)
        c2 = cloak.Cloak(percent=50)
        c3 = c1 + c2
        self.assertEqual(c3.percent, 50)
        c1 = cloak.Cloak(percent=20)
        c2 = cloak.Cloak(percent=50)
        c3 = c1 + c2
        self.assertEqual(c3.percent, 60)
        c3 = c2 + c1
        self.assertEqual(c3.percent, 60)
