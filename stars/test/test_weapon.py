import unittest
from unittest.mock import patch
from .. import *


class WeaponTestCase(unittest.TestCase):
    def test_accuracy1(self):
        w = weapon.Weapon(range_tm=1)
        self.assertEqual(w.get_accuracy(0), 100)

    def test_accuracy2(self):
        w = weapon.Weapon(range_tm=1)
        self.assertEqual(w.get_accuracy(1), 0)

    def test_accuracy3(self):
        w = weapon.Weapon(range_tm=1, is_beam=False)
        self.assertEqual(w.get_accuracy(0), 100)

    def test_accuracy4(self):
        w = weapon.Weapon(range_tm=1, is_beam=False)
        self.assertEqual(w.get_accuracy(stars_math.TERAMETER_2_LIGHTYEAR), 0)

    def test_accuracy5(self):
        w = weapon.Weapon(range_tm=2, is_beam=False)
        self.assertEqual(w.get_accuracy(stars_math.TERAMETER_2_LIGHTYEAR), 93.75)

    def test_power1(self):
        w = weapon.Weapon(power=100, range_tm=1)
        self.assertEqual(w.get_power(0, 150, 0), (100, 0))

    def test_power2(self):
        w = weapon.Weapon(power=100, range_tm=1)
        self.assertEqual(w.get_power(0, 50, 150), (50, 50))

    def test_power3(self):
        w = weapon.Weapon(power=100, range_tm=1)
        self.assertEqual(w.get_power(0, 0, 150), (0, 100))

    def test_power4(self):
        w = weapon.Weapon(power=100, range_tm=1)
        self.assertEqual(w.get_power(stars_math.TERAMETER_2_LIGHTYEAR, 0, 150), (0, 0))

    def test_power5(self):
        w = weapon.Weapon(power=100, range_tm=2)
        self.assertEqual(w.get_power(stars_math.TERAMETER_2_LIGHTYEAR, 50, 150), (50, 0))

    def test_power6(self):
        w = weapon.Weapon(power=100, range_tm=1, armor_multiplier=2)
        self.assertEqual(w.get_power(0, 50, 150), (50, 100))

    def test_power7(self):
        w = weapon.Weapon(power=100, range_tm=1, is_beam=False)
        self.assertEqual(w.get_power(0, 50, 150), (50, 50))

    def test_power8(self):
        w = weapon.Weapon(power=100, range_tm=1, is_beam=False)
        self.assertEqual(w.get_power(0, 150, 150), (75, 25))

    def test_power9(self):
        w = weapon.Weapon(power=100, range_tm=2, is_beam=False)
        self.assertEqual(w.get_power(stars_math.TERAMETER_2_LIGHTYEAR, 50, 150), (50, 50))

    def test_power10(self):
        w = weapon.Weapon(power=100, range_tm=1, is_beam=False, armor_multiplier=2)
        self.assertEqual(w.get_power(0, 150, 150), (75, 50))

    def test_damage1(self):
        w = weapon.Weapon(power=1, range_tm=1)
        self.assertNotEqual(w.get_damage(0, 100, 100, 2000, 0), (0, 0))

    def test_damage2(self):
        w = weapon.Weapon(power=1, range_tm=1)
        self.assertEqual(w.get_damage(1, 100, 100, 2000, 0), (0, 0))

    def test_damage3(self):
        with patch.object(weapon.Weapon, 'get_power', return_value=(1,1)) as mock:
            w = weapon.Weapon(power=1, range_tm=2, is_beam=False)
            for i in range(0, 100):
                w.get_damage(stars_math.TERAMETER_2_LIGHTYEAR, 100, 100, 0, 0)
            self.assertLess(mock.call_count, 100)
            self.assertGreater(mock.call_count, 80)

    def test_damage4(self):
        with patch.object(weapon.Weapon, 'get_power', return_value=(1,1)) as mock:
            w = weapon.Weapon(power=1, range_tm=2, is_beam=False)
            for i in range(0, 100):
                w.get_damage(stars_math.TERAMETER_2_LIGHTYEAR, 100, 100, 500, 100)
            self.assertLess(mock.call_count, 25)
            self.assertGreater(mock.call_count, 5)
