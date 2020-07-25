import unittest
from .. import *

class TestCombat(unittest.TestCase):
    def test_calc_strategy_m(self):
        everybody=[ship.Ship(location=location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0)), ship.Ship()]
        c = combat.Combat(everybody=everybody)
        strategy = c.calc_strategy_m(c.everybody[0])
        self.assertEqual(strategy[0], location.Location(x=0, y=0, z=0))
        self.assertEqual(strategy[1], True)
        strategy = c.calc_strategy_m(c.everybody[1])
        self.assertEqual(strategy[0], location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0))
        self.assertEqual(strategy[1], True)
    #def test_all():
    #    r = Combat()
    #    r.take_turn()
