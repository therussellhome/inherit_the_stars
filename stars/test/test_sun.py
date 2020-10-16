import unittest
from .. import *

class PlanetTestCase(unittest.TestCase):
        
    def test_get_color(self):
        s = sun.Sun()
        s.radiation = 100
        s.temperature = -50
        self.assertEqual(s.get_color(), '#FF8080')
        s.temperature = 150
        self.assertEqual(s.get_color(), '#9980FF')
        s.radiation = 0
        self.assertEqual(s.get_color(), '#AC9FDF')
        s.radiation = 50
        self.assertEqual(s.get_color(), '#A38FEF')
        s.temperature = 75
        self.assertEqual(s.get_color(), '#8FE1EF')
        s.radiation = 100
        self.assertEqual(s.get_color(), '#80ECFF')
        #reset gravity, temperature and radiation so other functions don't have problems
        s.gravity = 50
        s.temperature = 50
        s.radiation = 50
        self.assertEqual(s.get_color(), '#8FEF99')

    def test_colonize(self):
        p1 = player.Player(name='p1')
        r1 = reference.Reference(p1)
        p2 = player.Player(name='p2', race=race.Race(primary_race_trait = 'Pa\'anuri'))
        r2 = reference.Reference(p2)
        s = sun.Sun()
        s.colonize(r1)
        self.assertEqual(s.player.is_valid, False)
        s.colonize(r2)
        self.assertEqual(s.player.is_valid, True)
        self.assertEqual(s.player.name, 'p2')
