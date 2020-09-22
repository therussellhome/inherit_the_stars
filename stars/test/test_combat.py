import unittest
from .. import *
#from .. import weapon

class TestCombat(unittest.TestCase):
    def setUp(self):
        self.player1 = player.Player()
        self.player2 = player.Player()
    
    def test_calc_strategy_m(self):
        everybody=[
            ship.Ship(
                location=location.Location(
                    x=stars_math.TERAMETER_2_LIGHTYEAR
                    )
                ),
            ship.Ship()
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan())
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan())
        strategy = c.calc_strategy_m(c.everybody[0])
        self.assertEqual(strategy[0], location.Location(x=0, y=0, z=0))
        self.assertEqual(strategy[1], True)
        strategy = c.calc_strategy_m(c.everybody[1])
        self.assertEqual(strategy[0], location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0))
        self.assertEqual(strategy[1], True)
        everybody=[
            ship.Ship(
                weapons = [weapon.Weapon()],
                location=location.Location(
                    x=stars_math.TERAMETER_2_LIGHTYEAR)
                ),
            ship.Ship(
                weapons = [weapon.Weapon()]
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan(p_target='starbase', s_target='ship'))
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan(s_target='starbase', p_target='ship'))
        strategy = c.calc_strategy_m(c.everybody[0])
        self.assertEqual(strategy[0], location.Location(x=0, y=0, z=0))
        self.assertEqual(strategy[1], False)
        strategy = c.calc_strategy_m(c.everybody[1])
        self.assertEqual(strategy[0], location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0))
        self.assertEqual(strategy[1], False)
        everybody=[
            ship.Ship(
                weapons = [weapon.Weapon()],
                location=location.Location(
                    x=stars_math.TERAMETER_2_LIGHTYEAR),
                is_starbase = True
                ),
            ship.Ship(
                weapons = [weapon.Weapon()],
                is_starbase = True
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan(p_target='starbase', s_target='ship'))
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan(s_target='starbase', p_target='ship'))
        strategy = c.calc_strategy_m(c.everybody[0])
        self.assertEqual(strategy[0], location.Location(x=0, y=0, z=0))
        self.assertEqual(strategy[1], False)
        strategy = c.calc_strategy_m(c.everybody[1])
        print(strategy[0].__dict__)
        self.assertEqual(strategy[0], location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0))
        self.assertEqual(strategy[1], False)
        
    def test_move(self):
        everybody = [
            ship.Ship(
                location = location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR),
                weapons = [weapon.Weapon()],
                max_distance = stars_math.TERAMETER_2_LIGHTYEAR / 2
                ),
            ship.Ship(
                location = location.Location(),
                weapons = [weapon.Weapon()],
                max_distance = stars_math.TERAMETER_2_LIGHTYEAR / 2
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan())
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan())
        c.move(c.everybody[0])
        self.assertEqual(c.everybody[0].ship.location - location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR / 2), 0)
        c.move(c.everybody[1])
        self.assertEqual(c.everybody[1].ship.location - location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR / 2), 0)
        everybody = [
            ship.Ship(
                location = location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR),
                weapons = [weapon.Weapon()],
                max_distance = stars_math.TERAMETER_2_LIGHTYEAR / 2
                ),
            ship.Ship(
                location = location.Location(),
                weapons = [weapon.Weapon()],
                max_distance = stars_math.TERAMETER_2_LIGHTYEAR / 2
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan(standoff = 0.2))
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan(standoff = 0.2))
        c.move(c.everybody[0])
        self.assertEqual(c.everybody[0].ship.location - location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR / 2), 0)
        c.move(c.everybody[1])
        self.assertEqual(c.everybody[1].ship.location - location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR * 0.3), 0)
        everybody = [
            ship.Ship(
                location = location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR * 0.01),
                weapons = [weapon.Weapon()],
                max_distance = stars_math.TERAMETER_2_LIGHTYEAR / 2
                ),
            ship.Ship(
                location = location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR * -0.01),
                weapons = [weapon.Weapon()],
                max_distance = stars_math.TERAMETER_2_LIGHTYEAR / 2
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan(standoff = 0.2))
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan(standoff = 0.2))
        c.move(c.everybody[0])
        self.assertEqual(c.everybody[0].ship.location - location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR * 0.19), 0)
        c.move(c.everybody[1])
        self.assertEqual(c.everybody[1].ship.location - location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR * -0.01), 0)
        
    def test_calc_strategy_f(self):
        everybody=[
            ship.Ship(
                location=location.Location(
                    x=stars_math.TERAMETER_2_LIGHTYEAR),
                weapons=[weapon.Weapon()]
                ),
            ship.Ship(
                weapons=[weapon.Weapon()]
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan())
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan())
        strategy = c.calc_strategy_f(c.everybody[0])
        self.assertEqual(strategy, c.everybody[1])
        strategy = c.calc_strategy_f(c.everybody[1])
        self.assertEqual(strategy, c.everybody[0])
        everybody=[
            ship.Ship(
                location=location.Location(
                    x=stars_math.TERAMETER_2_LIGHTYEAR),
                weapons=[weapon.Weapon()]
                ),
            ship.Ship(
                weapons=[weapon.Weapon()]
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan(p_target='starbase', s_target='ship'))
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan(s_target='starbase', p_target='ship'))
        strategy = c.calc_strategy_f(c.everybody[0])
        self.assertEqual(strategy, c.everybody[1])
        strategy = c.calc_strategy_f(c.everybody[1])
        self.assertEqual(strategy, c.everybody[0])
        everybody=[
            ship.Ship(
                location=location.Location(
                    x=stars_math.TERAMETER_2_LIGHTYEAR
                    ),
                weapons=[weapon.Weapon()]
                ),
            ship.Ship(
                weapons=[weapon.Weapon()]
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan(p_target='starbase', s_target='ship', standoff=0.0, wait_until_closed_to_fire=True))
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan(s_target='starbase', p_target='ship', standoff=1, wait_until_closed_to_fire=True))
        strategy = c.calc_strategy_f(c.everybody[0])
        self.assertEqual(strategy, None)
        strategy = c.calc_strategy_f(c.everybody[1])
        self.assertEqual(strategy, c.everybody[0])
        everybody=[
            ship.Ship(
                location=location.Location(
                    x=stars_math.TERAMETER_2_LIGHTYEAR),
                weapons=[weapon.Weapon()],
                is_starbase = True
                ),
            ship.Ship(
                is_starbase = True,
                weapons=[weapon.Weapon()]
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan(p_target='starbase', s_target='ship'))
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan(s_target='starbase', p_target='ship'))
        strategy = c.calc_strategy_f(c.everybody[0])
        self.assertEqual(strategy, c.everybody[1])
        strategy = c.calc_strategy_f(c.everybody[1])
        self.assertEqual(strategy, c.everybody[0])
    
    def test_fire(self):
        everybody=[ship.Ship(armor=10, location=location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0), weapons=[weapon.Weapon(power=2, range_tm=2, armor_mutiplier=1)], max_distance=stars_math.TERAMETER_2_LIGHTYEAR/2), ship.Ship(armor=10, weapons=[weapon.Weapon(power=2, range_tm=2, armor_mutiplier=1)], max_distance=stars_math.TERAMETER_2_LIGHTYEAR/2)]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan())
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan())
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor, 9)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor, 9)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor, 8)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor, 8)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor, 7)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor, 7)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor, 6)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor, 6)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor, 5)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor, 5)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor, 4)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor, 4)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor, 3)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor, 3)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor, 2)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor, 2)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor, 1)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor, 1)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor, 0)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor, 1)
        c.move(c.everybody[0])
        c.fire(c.everybody[0])
    
    def test_all(self):
        everybody=[ship.Ship(location=location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0)), ship.Ship(location=location.Location(x=0, y=0, z=0))]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan())
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan())
        c.fight()
