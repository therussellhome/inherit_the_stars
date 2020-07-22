import unittest
from .. import * #importer's being grumpy

class ShipTestCase(unittest.TestCase):
    def setUp(self):
        s = ship.Ship()
        self.s = s
        # set up the ship for the waypoint
        s.x = 0
        s.y = 0
        s.z = 0
        s.waypoint_x = 100
        s.waypoint_y = 100
        s.waypoint_z = 100
        # set up for mining
        # set up the ship for the mining
        s.rate = 10
        # set up the planet for being mined
        p = planet.Planet()
        self.p = p
        p.titanium = .75
        p.silicon = .5
        p.lithium = 1
        p.size = 100
        p.colonized = False
        # set up for repairing
        # set up the ship for repairing
        s.repair_points = 20
        # set up the other ship for being repaired
        l = ship.Ship()
        self.l = l
        l.damage_points = 60
        """
        # set up for bombing
        # set up the ship for bombing
        s.bomb.percent_pop_kill = 3/10
        s.bomb.minimum_kill = 6000
        s.bomb.facility_kill = 200
        # set up the planet for being bombed
        t = planet.Planet()
        t.colonized = True
        t.num_colonists = 20000
        t.num_facilities = 800
        """
    def test_move(self):
        self.assertEqual(self.s.move(1), (1/173, 1/173, 1/173))
    def test_orbital_mining(self):
        self.assertEqual(self.s.orbital_mining(self.p).titanium, .675)# p.mineral = p.mineral - (kt_mined/p.size)
        self.assertEqual(self.s.orbital_mining(self.p).on_surface.titanium, 8)# kt_mined = rate * p.mineral
        self.assertEqual(self.s.orbital_mining(self.p).silicon, .45)
        self.assertEqual(self.s.orbital_mining(self.p).on_surface.silicon, 5)
        self.assertEqual(self.s.orbital_mining(self.p).lithium, .9)
        self.assertEqual(self.s.orbital_mining(self.p).on_surface.lithium, 10)
        self.p.silicon = 1
        self.assertEqual(self.s.orbital_mining(self.p).silicon, .9)
        self.assertEqual(self.s.orbital_mining(self.p).on_surface.silicon, 10)
        self.s.rate = 100
        self.p.size = 10000
        self.p.lithium = .9
        self.assertEqual(self.s.orbital_mining(self.p).titanium, .7425)
        self.assertEqual(self.s.orbital_mining(self.p).on_surface.titanium, 75)
        self.assertEqual(self.s.orbital_mining(self.p).silicon, .99)
        self.assertEqual(self.s.orbital_mining(self.p).on_surface.silicon, 100)
        self.assertEqual(self.s.orbital_mining(self.p).lithium, .891)
        self.assertEqual(self.s.orbital_mining(self.p).on_surface.lithium, 90)
        self.p.colonized = True
        self.p.titanium = 1
        self.p.lithium = .3
        self.p.silicon = .1
        self.p.size = 80
        self.s.rate = 50
        self.assertEqual(self.s.orbital_mining(self.p).titanium, 1)
        self.assertEqual(self.s.orbital_mining(self.p).on_surface.titanium, 0)
        self.assertEqual(self.s.orbital_mining(self.p).silicon, .1)
        self.assertEqual(self.s.orbital_mining(self.p).on_surface.silicon, 0)
        self.assertEqual(self.s.orbital_mining(self.p).lithium, .3)
        self.assertEqual(self.s.orbital_mining(self.p).on_surface.lithium, 0)
    def test_repair(self):
        """
        self.assertEqual(self.s.repair(self.l).damage_points, 40)
        self.assertEqual(self.s.repair(self.l).damage_points, 20)
        self.s.repair_points = 10
        self.l.damage_points = 90
        self.assertEqual(self.s.repair(self.l).damage_points, 80)
        self.s.repair_points = 25
        self.assertEqual(self.s.repair(self.l).damage_points, 55)
        self.s.repair_points = 44
        self.assertEqual(self.s.repair(self.l).damage_points, 11)
        self.l.damage_points = 0
        self.assertEqual(self.s.repair(self.l).damage_points, 0)
        """
        pass
    def test_bomb(self):
        """
        # test population bombing
        self.assertEqual(self.s.bomb(self.t).num_colonists, 6000)
        self.t.num_colonists = 30000
        self.assertEqual(self.s.bomb(self.t).num_colonists, 9000)
        self.t.num_colonists = 900
        self.assertEqual(self.s.bomb(self.t).num_colonists, 270)
        self.s.bomb.percent_pop_kill = 2/10
        self.assertEqual(self.s.bomb(self.t).num_colonists, 180)
        self.t.num_colonists = 1000
        self.s.bomb.percent_pop_kill = 1/10
        self.assertEqual(self.s.bomb(self.t).num_colonists, 100)
        self.s.bomb.percent_pop_kill = -.1
        self.t.num_colonists = 7000
        self.assertEqual(self.s.bomb(self.t).num_colonists, 1000)
        # test facility bombing
        self.assertEqual(self.s.bomb(self.t).num_facilities, 600)
        self.s.bomb.facility_kill = 300
        self.assertEqual(self.s.bomb(self.t).num_facilities, 300)
        self.t.num_facilities = 900
        self.assertEqual(self.s.bomb(self.t).num_facilities, 600)
        self.t.num_facilities = 100
        self.assertEqual(self.s.bomb(self.t).num_facilities, 0)
        self.s.bomb.facilaty_kill = 2000
        self.t.num_facilaties = 2500
        self.assertEqual(self.s.bomb(self.t).num_facilities, 500)
        self.t.num_facilaties = 900
        self.assertEqual(self.s.bomb(self.t).num_facilities, 0)
        """
        pass
