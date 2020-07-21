import unittest
from .. import *

class ScannerTestCase(unittest.TestCase):
    def setUp(self):
        s = scanner.Scanner()
        s.normal = 100
        s.penatrating = 75
        c = ship.Ship
        c.location.x = 100
        c.mass = 50
        c.cloak = 80
    def test_range_visible(self):
        # TODO
        pass
    def test_stack(self):
        # TODO
        pass
    def test_scan_ships(self):
        pass
    def test_scan_planets(self):
        pass
