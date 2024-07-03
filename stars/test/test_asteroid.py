import unittest
from .. import *


class AsteroidTestCase(unittest.TestCase):
    def test_get_speed01(self):
        a = asteroid.Asteroid()
        self.assertEqual(a.get_speed(), 0)

    def test_get_speed02(self):
        a = asteroid.Asteroid(ke=1, minerals=minerals.Minerals(titanium=2))
        self.assertEqual(a.get_speed(), 1)

    def test_get_speed03(self):
        a = asteroid.Asteroid(ke=16, minerals=minerals.Minerals(titanium=2))
        self.assertEqual(a.get_speed(), 2)

    def test_get_speed04(self):
        a = asteroid.Asteroid(ke=15, minerals=minerals.Minerals(titanium=2))
        self.assertEqual(a.get_speed(), 1)

    def test_get_speed05(self):
        a = asteroid.Asteroid()
        self.assertEqual(a.get_speed(), 0)

    def test_get_speed06(self):
        a = asteroid.Asteroid()
        self.assertEqual(a.get_speed(), 0)

