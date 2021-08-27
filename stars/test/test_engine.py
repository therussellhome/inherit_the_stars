import unittest
from .. import *

class EngineTestCase(unittest.TestCase):
    def test_tach100_1(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.speed_at_tach_100(100, [5, 0]), 9)

    def test_tach100_2(self):
        e = engine.Engine(kt_exponent=4.0, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.speed_at_tach_100(1000, [5, 0]), 1)

    def test_tachometer1(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(1, 100), 0)

    def test_tachometer2(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(2, 100), 0)

    def test_tachometer3(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(3, 100), 0)

    def test_tachometer4(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(4, 100), 1)

    def test_tachometer5(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(5, 100), 3)

    def test_tachometer6(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(6, 100), 7)

    def test_tachometer7(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(7, 100), 14)

    def test_tachometer8(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(8, 100), 26)

    def test_tachometer9(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(9, 100), 44)

    def test_tachometer10(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(10, 100), 71)

    def test_tachometer11(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(1, 500), 0)

    def test_tachometer12(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(2, 500), 0)

    def test_tachometer13(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(3, 500), 1)

    def test_tachometer14(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(4, 500), 5)

    def test_tachometer15(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(5, 500), 16)

    def test_tachometer16(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(6, 500), 40)

    def test_tachometer17(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(7, 500), 82)

    def test_tachometer18(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(8, 500), 153)

    def test_tachometer19(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(9, 500), 260)

    def test_tachometer20(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(10, 500), 417)

    def test_tachometer21(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(0, 100), 0)

    def test_tachometer22(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(10, 0), 0)

    def test_tachometer23(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(-10, -100), 0)

    def test_tachometer24(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.tachometer(-10, -100), 0)

    def test_tachometer25(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        # Hyper Denial
        self.assertEqual(e.tachometer(10, 100, [30, 0]), 326)

    def test_tachometer26(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        # Hyper Denial
        self.assertEqual(e.tachometer(10, 100, [60, 0]), 604)

    def test_fuel1(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(1, 100, 100), 0)

    def test_fuel2(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(2, 100, 100), 0)

    def test_fuel3(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(3, 100, 100), 0)

    def test_fuel4(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(4, 100, 100), 10000)

    def test_fuel5(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(5, 100, 100), 30000)

    def test_fuel6(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(6, 100, 100), 70000)

    def test_fuel7(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(7, 100, 100), 140000)

    def test_fuel8(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(8, 100, 100), 260000)

    def test_fuel9(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(9, 100, 100), 440000)

    def test_fuel10(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.fuel_calc(10, 100, 100), 710000)

    def test_fuel11(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        # Hyper Denial
        self.assertEqual(e.fuel_calc(10, 100, 100, [50, 0]), 5100000)

    def test_damage1(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.damage_calc(4, 100, 100), 0)

    def test_damage2(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.damage_calc(8, 500, 100), 20)

    def test_damage3(self):
        e = engine.Engine(kt_exponent=1.1, speed_divisor=11.0, speed_exponent=4.0)
        self.assertEqual(e.damage_calc(10, 100, 100, [50, 0]), 152)

    def test_siphon1(self):
        e = engine.Engine(antimatter_siphon=123)
        self.assertEqual(e.siphon_calc(1), 123)

    def test_siphon2(self):
        e = engine.Engine(antimatter_siphon=123)
        self.assertEqual(e.siphon_calc(3), 369)
