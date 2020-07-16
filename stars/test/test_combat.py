import unittest
from .. import *

class TestCombat(unittest.TestCase):
    def test_calc_strategy_m(self):
        l = location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0)
        ship1 = ship.Ship(location=l)
        everybody = [ship1, ship.Ship()]
        c = combat.Combat(everybody=everybody)
        self.assertEqual(c.calc_stategy_m(c.everybody[0]), (location.Location(0, 0, 0), True))
        self.assertEqual(c.calc_stategy_m(c.everybody[1]), (location.Location(stars_math.TERAMETER_2_LIGHTYEAR, 0, 0), True))
    #def test_all():
    #    r = Combat()
    #    r.take_turn()
