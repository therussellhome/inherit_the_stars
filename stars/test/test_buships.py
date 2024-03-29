import unittest
from .. import *

class BuShipsTestCase(unittest.TestCase):
    def test_init1(self):
        p = reference.Reference(planet.Planet(player=reference.Reference(player.Player())))
        b = buships.BuShips(planet=p)
        # Method does nothing so just verifying that no errors are thrown
        self.assertTrue(True)

    def test_init2(self):
        c = cost.Cost(energy=72, titanium=4)
        s = ship_design.ShipDesign(cost=c)
        b = buships.BuShips(ship_design=s, percent=25)
        c2 = cost.Cost(energy=54, titanium=3)
        self.assertEqual(b.cost, c2)

    def test_queue1(self):
        b = buships.BuShips()
        bs = b.queue(1)
        self.assertEqual(bs, 1)

    def test_queue2(self):
        b = buships.BuShips()
        bs = b.queue()
        self.assertNotEqual(bs, None) # Verify that a queue was created but details of it are not relevant
