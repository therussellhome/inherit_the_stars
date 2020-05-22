import unittest
from .. import *

class StarSystemTestCase(unittest.TestCase):
    def setUp(self):
        self.test_system = star_system.StarSystem(name='Tribond', num_planets=6)
        
    def _test_name_planet():
        self.assertEqual(self.test_system.name, 'Tribond')
        self.assertEqual(self.test_system.planets[0].name, "Tribond's Star")
        self.assertEqual(self.test_system.planets[1].name, 'Tribond I')
        self.assertEqual(self.test_system.planets[2].name, 'Tribond II')

