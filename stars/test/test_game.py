import unittest
from pathlib import Path
from .. import *


class GameTestCase(unittest.TestCase):
    def test_generate_turn(self):
        pass #TODO

    def test_init01(self):
        g = game.Game(num_systems=100)
        self.assertEqual(len(g.systems), 100)

    def test_init02(self):
        g = game.Game(x=0, y=0, z=0, num_systems=100)
        self.assertEqual(len(g.systems), 100)

    def test_init03(self):
        races = []
        for i in range(10):
            races.append(race.Race())
        g = game.Game(races=races, num_systems=0)
        self.assertEqual(len(g.systems), 10)

    def test_init04(self):
        blackholes = []
        for i in range(10):
            blackholes.append(blackhole.BlackHole())
        g = game.Game(races=[race.Race()], blackholes=blackholes, num_systems=1)
        self.assertEqual(len(g.players[0].intel), 11)
