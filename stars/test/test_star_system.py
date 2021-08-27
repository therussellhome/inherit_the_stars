import unittest
from .. import *

class StarSystemTestCase(unittest.TestCase):
    def test_ID_planet(self):
        s = star_system.StarSystem(ID='Tribond', num_planets=2)
        s.create_system(reference.Reference(race.Race()))
        self.assertEqual(s.ID, 'Tribond')
        self.assertEqual(s.planets[0].ID, "Tribond's Star")
        self.assertEqual(s.planets[1].ID, 'Tribond I')
        self.assertEqual(s.planets[2].ID, 'Tribond II')
