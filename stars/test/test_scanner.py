import unittest
from .. import *

class ScannerTestCase(unittest.TestCase):
    def test_range_visible1(self):
        s = scanner.Scanner()
        s.penetrating = 100
        self.assertEqual(s.range_visible(200), 100)

    def test_range_visible2(self):
        s = scanner.Scanner()
        s.normal = 100
        self.assertEqual(s.range_visible(200), 200)

    def test_range_visible3(self):
        s = scanner.Scanner()
        s.penetrating = 100
        s.normal = 200
        self.assertEqual(s.range_visible(200), 400)

    def test_add(self):
        s1 = scanner.Scanner()
        s1.penetrating = 200
        s2 = scanner.Scanner()
        s2.penetrating = 100
        s3 = s1 + s2
        self.assertEqual(s3.penetrating, 208.01)

    def test_reset_bins(self):
        scanner.reset_scan_bins([player.Player(), player.Player()])
        self.assertEqual(len(scanner._bin_testing()), 2)

    def test_binning1(self):
        p1 = player.Player()
        p_ref = reference.Reference(p1)
        scanner.reset_scan_bins([p1])
        obj = ship.Ship()
        scanner.bin_for_scanning(obj, location.Location(), 1, 1)
        self.assertEqual(len(scanner._bin_testing()[p_ref]), 1)

    def test_binning2(self):
        p1 = player.Player()
        p_ref = reference.Reference(p1)
        scanner.reset_scan_bins([p1])
        obj = ship.Ship()
        scanner.bin_for_scanning(obj, location.Location(), 1, 1)
        b = (0, 0, 0)
        self.assertEqual(len(scanner._bin_testing()[p_ref]), 1)
        self.assertEqual(len(scanner._bin_testing()[p_ref][b]), 1)
