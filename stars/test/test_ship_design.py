import unittest
from .. import *

class ShipDesignTestCase(unittest.TestCase):
    def test_armor_strength(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.armor, 0)
        s.add_component(tech.Tech(name='a123', armor=123))
        s.add_component(tech.Tech(name='a321', armor=321))
        self.assertEqual(s.armor, 444)

    def test_shield_strength(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.shield, 0)
        s.add_component(tech.Tech(name='s123', shield=123))
        s.add_component(tech.Tech(name='s321', shield=321))
        self.assertEqual(s.shield, 444)

    def test_cloak(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.cargo_max, 0)
        s.add_component(tech.Tech(name='c50', cloak=cloak.Cloak(percent=50)))
        s.add_component(tech.Tech(name='c50', cloak=cloak.Cloak(percent=50)))
        self.assertEqual(s.cloak.percent, 75)

    def test_cargo_max(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.cargo_max, 0)
        s.add_component(tech.Tech(name='cargo123', cargo_max=123))
        s.add_component(tech.Tech(name='cargo321', cargo_max=321))
        self.assertEqual(s.cargo_max, 444)

    def test_fuel_max(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.fuel_max, 0)
        s.add_component(tech.Tech(name='f123', fuel_max=123))
        s.add_component(tech.Tech(name='f321', fuel_max=321))
        self.assertEqual(s.fuel_max, 444)
