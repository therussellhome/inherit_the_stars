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
        self.assertTrue(len(g.players[0].intel) > 14)

    def test_is_ready_to_generate01(self):
        g = game.Game(races=[race.Race()])
        self.assertFalse(g.is_ready_to_generate())

    def test_is_ready_to_generate02(self):
        g = game.Game(races=[race.Race()])
        g.players[0].ready_to_generate = True
        self.assertTrue(g.is_ready_to_generate())

    def test_populated_planets_01(self):
        g = game.Game(races=[race.Race()])
        self.assertTrue(len(g.populated_planets()) == 1)

    def test_generate_hundreth01(self):
        g = game.Game()
        g.generate_hundreth()
        self.assertEqual(g.hundreth, 1)

    def test_generate_hundreth02(self):
        g = game.Game(hundreth=1)
        g.generate_hundreth()
        self.assertEqual(g.hundreth, 2)

    def test_generate_hundreth03(self):
        g = game.Game(races=[race.Race()], hundreth=99)
        g.players[0].date = '{:01.2f}'.format(float(g.players[0].date) + 0.99)
        g.generate_hundreth()
        self.assertEqual(g.hundreth, 100)

    def test_generate_hundreth04(self):
        f0 = fleet.Fleet()
        g = game.Game(races=[race.Race()], hundreth=99)
        g.players[0].date = '{:01.2f}'.format(float(g.players[0].date) + 0.99)
        g.players[0].fleets.append(f0)
        g.generate_hundreth()
        self.assertEqual(g.hundreth, 100)

    def test__combat01(self):
        g = game.Game()
        g._combat()
        return #TODO
        self.assertTrue(True)

    def test__check_for_winner01(self):
        g = game.Game(races=[race.Race()], hundreth=2100, victory_after=21)
        g._check_for_winner()
        self.assertEqual(g.hundreth, 2100)

