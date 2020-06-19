import unittest
from .. import *

class ShipDesignTestCase(unittest.TestCase):
    def setUp(self):
        s = ship_design.ShipDesign()
        s.components.append(component.Component())
        s.components.append(component.Component())
        # set up the armor
        s.hull.armor = 10
        s.components[0].armor = 15
        s.components[1].armor = 0
        # set up the shields
        s.hull.shield = 5
        s.components[0].shields = 20
        s.components[1].shields = 20
        # set up the cargo
        s.hull.cargo = 200
        s.components[0].cargo = 100
        s.components[1].cargo = 0
        # set up the fuel
        s.hull.fuel = 300
        s.components[0] = 50
        s.components[1] = 0
    def test_armor_strength(self):
        self.assertEqual(self.s.get_armor_strength(), 25)
        self.s.hull.armor = 20
        self.assertEqual(self.s.get_armor_strength(), 35)
        self.s.components[0].armor = 25
        self.s.hull.armor = 25
        self.assertEqual(self.s.get_armor_strength(), 50)
        self.s.components[1].armor = 10
        self.assertEqual(self.s.get_armor_strength(), 60)
    def test_shield_strength(self):
        self.assertEqual(self.s.get_shield_strength(), 45)
        self.s.hull.shields = 10
        self.assertEqual(self.s.get_shield_strength(), 50)
        self.s.components[0].shields = 10
        self.s.components[1].shields = 15
        self.assertEqual(self.s.get_shield_strength(), 35)
        self.s.hull.shields = 20
        self.assertEqual(self.s.get_shield_strength(), 45)
    def test_cargo_max(self):
        self.assertEqual(self.s.get_cargo_max(), 300)
        self.components[1].cargo = 100
        self.assertEqual(self.s.get_cargo_max(), 400)
        self.components[0].cargo = 50
        self.components[1].cargo = 50
        self.assertEqual(self.s.get_cargo_max(), 300)
        self.components[0].cargo = 0
        self.components[1].cargo = 0
        self.assertEqual(self.s.get_cargo_max(), 200)
    def test_fuel_max(self):
        self.assertEqual(self.s.get_fuel_max(), 350)
        self.hull.fuel = 100
        self.assertEqual(self.s.get_fuel_max(), 150)
        self.components[0] = 100
        self.components[1] = 100
        self.assertEqual(self.s.get_fuel_max(), 300)
        self.hull.fuel = 50
        self.assertEqual(self.s.get_fuel_max(), 250)
