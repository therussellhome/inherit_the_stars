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
        players = []
        for i in range(10):
            players.append(player.Player())
        g = game.Game(players=players, num_systems=0)
        self.assertEqual(len(g.systems), 10)
