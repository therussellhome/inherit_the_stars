import unittest
from .. import *

class IntelTestCase(unittest.TestCase):
    def test_add_report(self):
        i = intel.Intel()
        with self.assertRaises(KeyError):
            self.assertEqual(i.latest['something'], 0)
        self.assertEqual(len(i.reports), 0)
        i.add_report(something=123)
        self.assertEqual(len(i.reports), 1)
        self.assertEqual(i.latest['something'], 123)
        self.assertEqual(i.reports[0]['something'], 123)
        i.add_report(something=456)
        self.assertEqual(len(i.reports), 1)
        self.assertEqual(i.latest['something'], 456)
        self.assertEqual(i.reports[0]['something'], 456)
        i.add_report(something=789, date=1)
        self.assertEqual(len(i.reports), 2)
        self.assertEqual(i.reports[1]['something'], 456)
        i.add_report(something=999, date=0)
        self.assertEqual(len(i.reports), 2)

    def test_get(self):
        i = intel.Intel()
        self.assertEqual(i.get(attribute='something', default=999), 999)
        i.add_report(something=123, date=1)
        i.add_report(something=456, date=1.1)
        self.assertEqual(i.get(attribute='something', default=999), 456)
        self.assertEqual(i.get()['something'], 456)
        self.assertEqual(i.get(date=1, default=999)['something'], 123)
