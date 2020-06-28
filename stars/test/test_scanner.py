import unittest
from .. import *

class ScannerTestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(scanner.volume_add(0, 200), 200)
        self.assertEqual(scanner.volume_add(100, 200), 208.01)
