import unittest
from .. import *

class SunTestCase(unittest.TestCase):

    def test_get_color1(self):
        s = sun.Sun(gravity=50, radiation=100, temperature=-50)
        self.assertEqual(s.get_color(), '#FF8080')

    def test_get_color2(self):
        s = sun.Sun(gravity=50, radiation=100, temperature=150)
        self.assertEqual(s.get_color(), '#9980FF')

    def test_get_color3(self):
        s = sun.Sun(gravity=50, radiation=0, temperature=150)
        self.assertEqual(s.get_color(), '#AC9FDF')

    def test_get_color4(self):
        s = sun.Sun(gravity=50, radiation=50, temperature=150)
        self.assertEqual(s.get_color(), '#A38FEF')

    def test_get_color5(self):
        s = sun.Sun(gravity=50, radiation=50, temperature=75)
        self.assertEqual(s.get_color(), '#8FE1EF')

    def test_get_color6(self):
        s = sun.Sun(gravity=50, radiation=100, temperature=75)
        self.assertEqual(s.get_color(), '#80ECFF')

    def test_get_color7(self):
        s = sun.Sun(gravity=50, radiation=50, temperature=50)
        self.assertEqual(s.get_color(), '#8FEF99')


    def test_colonize1(self):
        s = sun.Sun()
        self.assertFalse(s.colonize(player.Player(), 'a minister'))

    def test_colonize2(self):
        s = sun.Sun()
        self.assertTrue(s.colonize(player.Player(race=race.Race(primary_race_trait='Pa\'anuri')), 'a minister'))
