import unittest
from .. import *


class AsteroidTestCase(unittest.TestCase):
    def test__init__01(self):
        a = asteroid.Asteroid()
        self.assertEqual(a.decay_factor, 0.01)
        self.assertEqual(a.minerals.sum(), 0)

    def test__init__02(self):
        a = asteroid.Asteroid(titanium=1)
        self.assertEqual(a.minerals.titanium, 1)
        self.assertEqual(a.minerals.sum(), 1)

    def test__init__03(self):
        a = asteroid.Asteroid(location=location.Location(0, 0, 1))
        self.assertEqual(a.location - a.target, 1)
        self.assertEqual(a.minerals.sum(), 0)

    def test__init__04(self):
        a = asteroid.Asteroid(minerals=minerals.Minerals(silicon=1))
        self.assertEqual(a.minerals.silicon, 1)
        self.assertEqual(a.minerals.sum(), 1)

    def test_get_speed00(self):
        a = asteroid.Asteroid()
        self.assertEqual(a.get_speed(), 0)

    def test_get_speed01(self):
        a = asteroid.Asteroid(minerals=minerals.Minerals(titanium=2))
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
        a = asteroid.Asteroid(ke=19, minerals=minerals.Minerals(titanium=3))
        self.assertEqual(a.get_speed(), 1)

    def test_move01(self):
        a = asteroid.Asteroid(ke=16, minerals=minerals.Minerals(titanium=2), location=location.Location(4, 7, 0), target=location.Location(4, 0, 0))
        a.move()
        self.assertEqual(a.location.xyz, (4, 3, 0))
        self.assertEqual(a.away, False)

    def test_move02(self):
        a = asteroid.Asteroid(ke=16, minerals=minerals.Minerals(titanium=2), location=location.Location(4, 3, 0), target=location.Location(4, 0, 0))
        a.move()
        self.assertEqual(a.location.xyz, (4, -1, 0))

    def test_move03(self):
        p = planet.Planet(location=location.Location(4, 0, 0))
        a = asteroid.Asteroid(ke=16, minerals=minerals.Minerals(titanium=2), location=location.Location(4, 7, 0), target=location.Location(reference=p))
        a.move()
        self.assertEqual(a.location.xyz, (4, 3, 0))
        self.assertEqual(a.away, False)

    def test_move04(self):
        p = planet.Planet(location=location.Location(4, 0, 0))
        a = asteroid.Asteroid(ke=16, minerals=minerals.Minerals(titanium=2), location=location.Location(4, 3, 0), target=location.Location(reference=p))
        a.move()
        self.assertEqual(a.location.xyz, (4, 0, 0))
        self.assertEqual(a.away, False)
