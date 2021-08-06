import unittest
from .. import *

class EngineTestCase(unittest.TestCase):
    def test_tach100_1(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.speed_at_tach_100(100, 5), 5)

    def test_tach100_2(self):
        e = engine.Engine(kt_exponent=4.0, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.speed_at_tach_100(1000, 5), 1)

    def test_tachometer(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(1, 100, 0), 0)
        self.assertEqual(e.tachometer(2, 100, 0), 0)
        self.assertEqual(e.tachometer(3, 100, 0), 0)
        self.assertEqual(e.tachometer(4, 100, 0), 1)
        self.assertEqual(e.tachometer(5, 100, 0), 3)
        self.assertEqual(e.tachometer(6, 100, 0), 7)
        self.assertEqual(e.tachometer(7, 100, 0), 14)
        self.assertEqual(e.tachometer(8, 100, 0), 26)
        self.assertEqual(e.tachometer(9, 100, 0), 44)
        self.assertEqual(e.tachometer(10, 100, 0), 71)
        self.assertEqual(e.tachometer(1, 500, 0), 0)
        self.assertEqual(e.tachometer(2, 500, 0), 0)
        self.assertEqual(e.tachometer(3, 500, 0), 1)
        self.assertEqual(e.tachometer(4, 500, 0), 5)
        self.assertEqual(e.tachometer(5, 500, 0), 16)
        self.assertEqual(e.tachometer(6, 500, 0), 40)
        self.assertEqual(e.tachometer(7, 500, 0), 82)
        self.assertEqual(e.tachometer(8, 500, 0), 153)
        self.assertEqual(e.tachometer(9, 500, 0), 260)
        self.assertEqual(e.tachometer(10, 500, 0), 417)
        self.assertEqual(e.tachometer(0, 100, 0), 0)
        self.assertEqual(e.tachometer(10, 0, 0), 0)
        self.assertEqual(e.tachometer(-10, -100, 0), 0)
        # Hyper Denial
        self.assertEqual(e.tachometer(10, 100, 1), 894)
        self.assertEqual(e.tachometer(10, 100, 2), 1397)

    def test_fuel(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(1, 100, 0, 100), 0)
        self.assertEqual(e.fuel_calc(2, 100, 0, 100), 0)
        self.assertEqual(e.fuel_calc(3, 100, 0, 100), 0)
        self.assertEqual(e.fuel_calc(4, 100, 0, 100), 10000)
        self.assertEqual(e.fuel_calc(5, 100, 0, 100), 30000)
        self.assertEqual(e.fuel_calc(6, 100, 0, 100), 70000)
        self.assertEqual(e.fuel_calc(7, 100, 0, 100), 140000)
        self.assertEqual(e.fuel_calc(8, 100, 0, 100), 260000)
        self.assertEqual(e.fuel_calc(9, 100, 0, 100), 440000)
        self.assertEqual(e.fuel_calc(10, 100, 0, 100), 710000)
        # Hyper Denial
        self.assertEqual(e.fuel_calc(10, 100, 1, 100), 8940000)

    def test_damage(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.damage_calc(4, 100, 0, 100), 0)
        self.assertEqual(e.damage_calc(8, 500, 0, 100), 20)
        self.assertEqual(e.damage_calc(10, 100, 1, 100), 294)

    def test_siphon(self):
        e = engine.Engine(antimatter_siphon=123)
        self.assertEqual(e.siphon_calc(1), 123)
        self.assertEqual(e.siphon_calc(3), 369)
        pass

