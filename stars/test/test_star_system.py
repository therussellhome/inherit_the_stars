import unittest
from .. import *

class StarSystemTestCase(unittest.TestCase):
    def test_name_planet(self):
        s = star_system.StarSystem(name='Tribond')
        s.create_system(reference.Reference(player.Player()))
        self.assertEqual(s.name, 'Tribond')
        self.assertEqual(s.planets[0].name, "Tribond's Star")
        self.assertEqual(s.planets[1].name, 'Tribond I')
        self.assertEqual(s.planets[2].name, 'Tribond II')
