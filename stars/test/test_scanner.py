import unittest
from .. import *

class ScannerTestCase(unittest.TestCase):
    def test_add(self):
        s1 = scanner.Scanner()
        s1.penetrating = 200
        s2 = scanner.Scanner()
        s2.penetrating = 100
        s3 = s1 + s2
        self.assertEqual(s3.penetrating, 208.01)
