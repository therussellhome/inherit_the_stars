from .combat import Combat
from .ship import Ship
from .stars_math import TERAMETER_2_LIGHTYEAR

class TestCombat():
    def test_calc_strategy_m():
        c = Combat(everybody=[Ship(location=Location(TERAMETER_2_LIGHTYEAR, 0, 0)), Ship()])
        self.assertEqual(c.calc_stategy_m(c.everybody[0]), (Location(0, 0, 0), True))
        self.assertEqual(c.calc_stategy_m(c.everybody[1]), (Location(TERAMETER_2_LIGHTYEAR, 0, 0), True))
    #def test_all():
    #    r = Combat()
    #    r.take_turn()
