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
    def test_move(self):
        everybody=[ship.Ship(location=location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0), weapons=[weapon.weapon()], max_distance=stars_math.TERAMETER_2_LIGHTYEAR/2), ship.Ship(weapons=[weapon.wepon()], max_distance=stars_math.TERAMETER_2_LIGHTYEAR/2)]
        c = combat.Combat(everybody=everybody)
        c.move(c.everybody[0])
        self.assertEqual(c.everybody[0].location, location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR/2, y=0, z=0))
        c.move(c.everybody[1])
        self.assertEqual(c.everybody[1].location, location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR/2, y=0, z=0))
    def test_calc_strategy_f(self):
        everybody=[ship.Ship(location=location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0), weapons=[weapon.weapon()]), ship.Ship(weapons=[weapon.weapon()])]
        c = combat.Combat(everybody=everybody)
        strategy = c.calc_strategy_f(c.everybody[0], c.everybody[0].wepons[0])
        self.assertEqual(strategy, c.everybody[1])
        strategy = c.calc_strategy_f(c.everybody[1], c.everybody[1].wepons[0])
        self.assertEqual(strategy[0], c.everybody[0])
    def test_fire(self):
        everybody=[ship.Ship(location=location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0), weapons=[weapon.weapon(power=2, range_tm=2, armor_mutiplier=1)], max_distance=stars_math.TERAMETER_2_LIGHTYEAR/2), ship.Ship(weapons=[weapon.weapon(power=2, range_tm=2, armor_mutiplier=1)], max_distance=stars_math.TERAMETER_2_LIGHTYEAR/2)]
        c = combat.Combat(everybody=everybody)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].armor, 9)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].armor, 9)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].armor, 8)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].armor, 8)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].armor, 7)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].armor, 7)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].armor, 6)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].armor, 6)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].armor, 5)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].armor, 5)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].armor, 4)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].armor, 4)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].armor, 3)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].armor, 3)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].armor, 2)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].armor, 2)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].armor, 1)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].armor, 1)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].armor, 0)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].armor, 1)
    def test_all(self):
        everybody=[ship.Ship(location=location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0), weapons=[weapon.weapon()]), ship.Ship(weapons=[weapon.weapon()])]
        c = Combat(everybody=everybody)
        c.take_turn()










