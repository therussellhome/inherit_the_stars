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
                    x=stars_math.TERAMETER_2_LIGHTYEAR),
                ),
            ship.Ship(
                weapons = [weapon.Weapon()],
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
                is_starbase = True,
                ),
            ship.Ship(
                weapons = [weapon.Weapon()],
                is_starbase = True,
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan(p_target='starbase', s_target='ship'))
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan(s_target='starbase', p_target='ship'))
        strategy = c.calc_strategy_m(c.everybody[0])
        self.assertEqual(strategy[0], location.Location(x=0, y=0, z=0))
        self.assertEqual(strategy[1], False)
        strategy = c.calc_strategy_m(c.everybody[1])
        #print(strategy[0].__dict__)
        self.assertEqual(strategy[0], location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0))
        self.assertEqual(strategy[1], False)
        
    def test_move(self):
        everybody = [
            ship.Ship(
                location = location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR),
                weapons = [weapon.Weapon()],
                engines = [engine.Engine(kt_exponent=2, speed_exponent=2, speed_divisor=9)],
                mass = 10,
                ),
            ship.Ship(
                location = location.Location(),
                weapons = [weapon.Weapon()],
                engines = [engine.Engine(kt_exponent=2, speed_exponent=2, speed_divisor=9)],
                mass = 10,
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
                engines = [engine.Engine(kt_exponent=2, speed_exponent=2, speed_divisor=9)],
                mass = 10,
                ),
            ship.Ship(
                location = location.Location(),
                weapons = [weapon.Weapon()],
                mass = 0,
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan())
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan())
        c.everybody[1].hidden_from.append(c.everybody[0].player)
        c.move(c.everybody[0])
        self.assertEqual(c.everybody[0].ship.location - location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR), 0)
        c.move(c.everybody[1])
        #print(stars_math.TERAMETER_2_LIGHTYEAR/20)
        #print(c.everybody[1].ship.location.__dict__, '', location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR / 20).__dict__)
        self.assertEqual(round(c.everybody[1].ship.location - location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR / 20), 20), 0)
        
        everybody = [
            ship.Ship(
                location = location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR),
                weapons = [weapon.Weapon()],
                engines = [engine.Engine(kt_exponent=2, speed_exponent=2, speed_divisor=9)],
                mass = 10,
                ),
            ship.Ship(
                location = location.Location(),
                weapons = [weapon.Weapon()],
                engines = [engine.Engine(kt_exponent=2, speed_exponent=2, speed_divisor=9)],
                mass = 10,
                )
            ]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan(standoff = 0.2))
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan(standoff = 0.2))
        a = c.everybody[0].ship.location.__dict__
        c.move(c.everybody[0])
        #print(c.everybody[0].ship.location.__dict__, a, location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR / 20).__dict__)
        self.assertEqual(c.everybody[0].ship.location - location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR / 2), 0)
        c.move(c.everybody[1])
        self.assertEqual(c.everybody[1].ship.location - location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR * 0.3), 0)
        everybody = [
            ship.Ship(
                location = location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR * 0.01),
                weapons = [weapon.Weapon()],
                engines = [engine.Engine(kt_exponent=2, speed_exponent=2, speed_divisor=9)],
                mass = 10,
                ),
            ship.Ship(
                location = location.Location(x = stars_math.TERAMETER_2_LIGHTYEAR * -0.01),
                weapons = [weapon.Weapon()],
                engines = [engine.Engine(kt_exponent=2, speed_exponent=2, speed_divisor=9)],
                mass = 10,
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
        everybody=[
            ship.Ship(
                armor=10,
                location=location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR),
                weapons=[weapon.Weapon(
                    power=2,
                    range_tm=2,
                    armor_mutiplier=1)],
                engines = [engine.Engine(kt_exponent=2, speed_exponent=2, speed_divisor=9)],
                mass = 10,
                ),
            ship.Ship(
                armor=10,
                weapons=[weapon.Weapon(
                    power=2,
                    range_tm=2,
                    armor_mutiplier=1)],
                engines = [engine.Engine(kt_exponent=2, speed_exponent=2, speed_divisor=9)],
                mass = 10,
                )]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan())
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan())
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor_damage, 1)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor_damage, 1)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor_damage, 2)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor_damage, 2)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor_damage, 3)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor_damage, 3)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor_damage, 4)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor_damage, 4)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor_damage, 5)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor_damage, 5)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor_damage, 6)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor_damage, 6)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor_damage, 7)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor_damage, 7)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor_damage, 8)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor_damage, 8)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor_damage, 9)
        c.fire(c.everybody[1])
        self.assertEqual(c.everybody[0].ship.armor_damage, 9)
        c.fire(c.everybody[0])
        self.assertEqual(c.everybody[1].ship.armor_damage, 10)
        try:
            c.fire(c.everybody[1])
            s = 'ship exists'
        except:
            s = 'ship is gone'
        self.assertEqual(s, 'ship is gone')
        c.move(c.everybody[0])
        c.fire(c.everybody[0])
    
    def test_all(self):
        everybody=[ship.Ship(location=location.Location(x=stars_math.TERAMETER_2_LIGHTYEAR, y=0, z=0)), ship.Ship(location=location.Location(x=0, y=0, z=0))]
        c = combat.Combat()
        c.add_ship(everybody[0], self.player1, battle_plan.BattlePlan())
        c.add_ship(everybody[1], self.player2, battle_plan.BattlePlan())
        #c.turn()
        c.fight()
