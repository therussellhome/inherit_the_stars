import unittest
from .. import *

class ShipDesignTestCase(unittest.TestCase):
    def test_armor_strength(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.armor, 0)
        s.add_component(tech.Tech(armor=123))
        s.add_component(tech.Tech(armor=321))
        self.assertEqual(s.armor, 444)

    def test_shield_strength(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.shield, 0)
        s.add_component(tech.Tech(shield=123))
        s.add_component(tech.Tech(shield=321))
        self.assertEqual(s.shield, 444)

    def test_cloak(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.cargo_max, 0)
        s.add_component(tech.Tech(cloak=cloak.Cloak(percent=50)))
        s.add_component(tech.Tech(cloak=cloak.Cloak(percent=50)))
        self.assertEqual(s.cloak.percent, 75)

    def test_cargo_max(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.cargo_max, 0)
        s.add_component(tech.Tech(cargo_max=123))
        s.add_component(tech.Tech(cargo_max=321))
        self.assertEqual(s.cargo_max, 444)

    def test_fuel_max(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.fuel_max, 0)
        s.add_component(tech.Tech(fuel_max=123))
        s.add_component(tech.Tech(fuel_max=321))
        self.assertEqual(s.fuel_max, 444)
