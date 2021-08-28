import unittest
from .. import *

class IntelTestCase(unittest.TestCase):
    def test_add_report1(self):
        i = intel.Intel(name='abc')
        i.add_report(reference.Reference('Ship/1'), '3001', {'location': location.Location(x=1, y=1, z=1), 'mass': 3})
        self.assertEqual(i.name, 'abc')
        self.assertEqual(i.location, (1, 1, 1))
        self.assertEqual(i.mass, 3)

    def test_add_report2(self):
        i = intel.Intel(name='abc')
        i.add_report(reference.Reference('Ship/1'), '3001', {'location': location.Location(x=1, y=1, z=1), 'mass': 3})
        i.add_report(reference.Reference('Ship/1'), '3001', {'location': location.Location(x=2, y=2, z=2), 'mass': 6})
        self.assertEqual(i.name, 'abc')
        self.assertEqual(i.location, (2, 2, 2))
        self.assertEqual(i.mass, 6)

    def test_add_report3(self):
        i = intel.Intel(name='abc')
        i.add_report(reference.Reference('Ship/1'), '2001', {'location': location.Location(x=1, y=1, z=1), 'mass': 3})
        i.add_report(reference.Reference('Ship/1'), '3001', {'location': location.Location(x=2, y=2, z=2), 'mass': 6})
        self.assertEqual(i.name, 'abc')
        self.assertEqual(i.location, (2, 2, 2))
        self.assertEqual(i.mass, 6)
        self.assertEqual(i.location_root['2001'], (1, 1, 1))
        self.assertEqual(i.location_root['3001'], (2, 2, 2))
