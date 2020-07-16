from .. import *

class TestCombat():
    def test_calc_strategy_m():
        c = combat.Combat(everybody=[ship.Ship(location=location.Location(stars_math.TERAMETER_2_LIGHTYEAR, 0, 0)), ship.Ship()])
        self.assertEqual(c.calc_stategy_m(c.everybody[0]), (location.Location(0, 0, 0), True))
        self.assertEqual(c.calc_stategy_m(c.everybody[1]), (location.Location(stars_math.TERAMETER_2_LIGHTYEAR, 0, 0), True))
    #def test_all():
    #    r = Combat()
    #    r.take_turn()
