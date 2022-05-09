import unittest
import math
from pathlib import Path
from .. import *
from ..hyperdenial import __denials as h__denials

class HyperDenialTestCase(unittest.TestCase):
    #testing reset
    def test_reset(self):
        h = hyperdenial.HyperDenial()
        hyperdenial.reset()

    def test_init01(self):
        h = hyperdenial.HyperDenial(radius=100)
        self.assertEqual(h.radius, 100)

    def test_add_1(self):
        h1 = hyperdenial.HyperDenial(radius=30)
        h2 = hyperdenial.HyperDenial(radius=30)
        h3 = hyperdenial.HyperDenial(radius=30)
        h4 = hyperdenial.HyperDenial(radius=30)
        h = h1+h2+h3+h4
        h += h
        self.assertEqual(h.radius, 60)
    
    def test_effect_1(self):
        h = hyperdenial.HyperDenial(radius=0)
        self.assertEqual(h.effect(1), 0)
    
    def test_effect_2(self):
        h = hyperdenial.HyperDenial(radius=0)
        self.assertEqual(h.effect(0), 0)
    
    def test_effect_3(self):
        h = hyperdenial.HyperDenial(radius=2)
        val = (4.0 / 3.0 * math.pi * ((2/max(1, 1.0001)) ** 3.0)) - 4.15
        self.assertEqual(h.effect(1.0001), val)

    def test_activate_1(self):
        hyperdenial.reset()
        h = hyperdenial.HyperDenial(radius=1)
        h.activate(None, location.Location(0, 1, 0))
        h_denials = getattr(hyperdenial, '__denials')
        self.assertEqual(h_denials[(None, location.Location(0, 1, 0).xyz)].radius, h.radius)
    
    def test_activate_2(self):
        hyperdenial.reset()
        h = hyperdenial.HyperDenial(radius=1)
        for i in range(8):
            h.activate(None, location.Location(0, 1, 0))
        h_denials = getattr(hyperdenial, '__denials')
        self.assertEqual(h_denials[(None, location.Location(0, 1, 0).xyz)].radius, h.radius * 2, 'Do we need to stop rounding in stars_math.volume_add?')
    
    def test_activate_3(self):
        hyperdenial.reset()
        h = hyperdenial.HyperDenial(radius=1)
        h.activate(None, location.Location(0, 1, 0))
        hyperdenial.HyperDenial(radius=10).activate(None, location.Location(0, 1, 0))
        h_denials = getattr(hyperdenial, '__denials')
        self.assertEqual(h_denials[(None, location.Location(0, 1, 0).xyz)].radius, stars_math.volume_add(h.radius, 10))
    
    def test_activate_4(self):
        hyperdenial.reset()
        h = hyperdenial.HyperDenial(radius=1)
        p1 = reference.Reference(player.Player())
        for i in range(8):
            h.activate(p1, location.Location(0, 1, 0))
        hyperdenial.HyperDenial(radius=10).activate(None, location.Location(0, 1, 0))
        h_denials = getattr(hyperdenial, '__denials')
        self.assertEqual(h_denials[(p1, location.Location(0, 1, 0).xyz)].radius, h.radius*2, 'Do we need to stop rounding in stars_math.volume_add?')
    

        self.assertEqual(h_denials[(None, location.Location(0, 1, 0).xyz)].radius, 10)
    
    def test_reset_1(self):
        hyperdenial.reset()
        h = hyperdenial.HyperDenial(radius=1)
        for i in range(8):
            h.activate(None, location.Location(0, 1, 0))
        hyperdenial.HyperDenial(radius=10).activate(None, location.Location(0, 1, 0))
        h_denials = getattr(hyperdenial, '__denials')
        print(h_denials)
        hyperdenial.reset()
        h_denials = getattr(hyperdenial, '__denials')
        print(h_denials)
        self.assertEqual(len(h_denials), 0)
    
    def test_calc_blackhole_1(self):
        hyperdenial.reset()
        hyperdenial.HyperDenial(radius=10).activate(None, location.Location(0, 1, 0))
        h_denials = getattr(hyperdenial, '__denials')
        print(h_denials)
        p1 = player.Player()
        fleet_1 = fleet.Fleet(location=location.Location(1, 1, 1), player=p1, ships=[ship.Ship(engines=[engine.Engine()], fuel_max=1000000, fuel = 1000000)], orders=[order.Order(location=location.Location(1, 0, 0), speed=-1)])
        fleet_1.read_orders()
        print(fleet_1.is_stationary)
        hyperdenial.calc([fleet_1])
        self.assertEqual(fleet_1.hyperdenial_effect[1], stars_math.volume(10/math.sqrt(2)) - 4.15)
    
    def test_calc_blackhole_2(self):
        hyperdenial.reset()
        hyperdenial.HyperDenial(radius=10).activate(None, location.Location(0, 1, 0))
        h_denials = getattr(hyperdenial, '__denials')
        print(h_denials)
        p1 = player.Player()
        fleet_1 = fleet.Fleet(location=location.Location(1, 1, 1), player=p1, ships=[ship.Ship(engines=[engine.Engine()], fuel_max=1000000, fuel = 1000000)], orders=[order.Order(location=location.Location(1, 0, 0), speed=-1)])
        fleet_2 = fleet.Fleet(location=location.Location(1, 1, 1), player=p1, ships=[ship.Ship(engines=[engine.Engine()], fuel_max=1000000, fuel = 1000000)], orders=[order.Order(location=location.Location(0, 0, 1), speed=-1)])
        fleet_1.read_orders()
        fleet_2.read_orders()
        print(fleet_1.is_stationary)
        hyperdenial.calc([fleet_1, fleet_2])
        print(math.sqrt(2))
        l1 = location.Location(0, 1, 0)
        l2 = location.Location(1, 1, 1)
        print(l1 - l2)
        self.assertEqual(fleet_1.hyperdenial_effect[1], stars_math.volume(10/math.sqrt(2)) - 4.15)
        self.assertEqual(fleet_2.hyperdenial_effect[1], stars_math.volume(10/math.sqrt(2)) - 4.15)

    def test_calc_player_1(self):
        hyperdenial.reset()
        p1 = player.Player()
        hyperdenial.HyperDenial(radius=10).activate(p1, location.Location(0, 1, 0))
        h_denials = getattr(hyperdenial, '__denials')
        print(h_denials)
        p2 = player.Player()
        fleet_1 = fleet.Fleet(location=location.Location(1, 1, 1), player=p1, ships=[ship.Ship(engines=[engine.Engine()], fuel_max=1000000, fuel = 1000000)], orders=[order.Order(location=location.Location(1, 0, 0), speed=-1)])
        fleet_2 = fleet.Fleet(location=location.Location(1, 1, 1), player=p2, ships=[ship.Ship(engines=[engine.Engine()], fuel_max=1000000, fuel = 1000000)], orders=[order.Order(location=location.Location(0, 0, 1), speed=-1)])
        fleet_1.read_orders()
        fleet_2.read_orders()
        print(fleet_1.is_stationary)
        hyperdenial.calc([fleet_1, fleet_2])
        print(math.sqrt(2))
        l1 = location.Location(0, 1, 0)
        l2 = location.Location(1, 1, 1)
        print(l1 - l2)
        self.assertEqual(fleet_1.hyperdenial_effect[1], 0)
        self.assertEqual(fleet_2.hyperdenial_effect[1], stars_math.volume(10/math.sqrt(2)) - 4.15)
