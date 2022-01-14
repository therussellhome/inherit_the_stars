import unittest
from .. import *

class ScanTestCase(unittest.TestCase):
    def test_reset(self):
        scan.reset([player.Player(), player.Player()], [], [], [], [], [], [])
        self.assertEqual(len(scan._bin_testing()), 2)

    def test_binning1(self):
        p1 = player.Player()
        p_ref = reference.Reference(p1)
        s = ship.Ship()
        f = fleet.Fleet() + s
        scan.reset([p1], [f], [], [], [], [], [])
        self.assertEqual(len(scan._bin_testing()[p_ref]), 1)

    def test_binning2(self):
        p1 = player.Player()
        p_ref = reference.Reference(p1)
        s = ship.Ship()
        f = fleet.Fleet() + s
        scan.reset([p1], [f], [], [], [], [], [])
        b = (0, 0, 0)
        self.assertEqual(len(scan._bin_testing()[p_ref]), 1)
        self.assertEqual(len(scan._bin_testing()[p_ref][b]), 1)
