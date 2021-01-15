import unittest
from .. import *

class ShipDesignTestCase(unittest.TestCase):
    def test_hull(self):
        s = ship_design.ShipDesign()
        s.set_hull(tech.Tech(ID='hull', armor=321))
        self.assertEqual(s.armor, 321)

    def test_armor_strength(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.armor, 0)
        s.add_component(tech.Tech(ID='a123', armor=123))
        s.add_component(tech.Tech(ID='a123', armor=123))
        self.assertEqual(s.armor, 246)

    def test_shield_strength(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.shield, 0)
        s.add_component(tech.Tech(ID='s123', shield=123))
        s.add_component(tech.Tech(ID='s321', shield=321))
        self.assertEqual(s.shield, 444)

    def test_cloak(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.cargo_max, 0)
        s.add_component(tech.Tech(ID='c50', cloak=cloak.Cloak(percent=50)))
        s.add_component(tech.Tech(ID='c50', cloak=cloak.Cloak(percent=50)))
        self.assertEqual(s.cloak.percent, 75)

    def test_cargo_max(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.cargo_max, 0)
        s.add_component(tech.Tech(ID='cargo123', cargo_max=123))
        s.add_component(tech.Tech(ID='cargo321', cargo_max=321))
        self.assertEqual(s.cargo_max, 444)

    def test_fuel_max(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.fuel_max, 0)
        s.add_component(tech.Tech(ID='f123', fuel_max=123))
        s.add_component(tech.Tech(ID='f321', fuel_max=321))
        self.assertEqual(s.fuel_max, 444)

    def test_remove1(self):
        s = ship_design.ShipDesign()
        s.add_component(tech.Tech(ID='a123', armor=123))
        s.add_component(tech.Tech(ID='a321', armor=321))
        self.assertEqual(s.armor, 444)
        s.remove_component(tech.Tech(ID='a321', armor=321))
        self.assertEqual(s.armor, 123)

    def test_remove2(self):
        s = ship_design.ShipDesign()
        t = tech.Tech(ID='a123', armor=123)
        s.add_component(t)
        s.add_component(t)
        s.remove_component(t)
        s.remove_component(t)
        s.remove_component(t)
        self.assertEqual(s.armor, 0)

    def test_valid1(self):
        s = ship_design.ShipDesign()
        s.set_hull(tech.Tech(ID='hull1', slots_general=1))
        self.assertTrue(s.is_valid())

    def test_valid2(self):
        s = ship_design.ShipDesign()
        s.set_hull(tech.Tech(ID='hull1', slots_general=1))
        s.add_component(tech.Tech(ID='a123', armor=123))
        s.add_component(tech.Tech(ID='a123', armor=123))
        self.assertFalse(s.is_valid())

    def test_valid3(self):
        s = ship_design.ShipDesign()
        l = tech_level.TechLevel()
        s.set_hull(tech.Tech(ID='hull2', slots_general=1))
        s.hull.level.energy = 10
        self.assertFalse(s.is_valid(level=l))

    def test_valid4(self):
        s = ship_design.ShipDesign()
        t = tech.Tech(ID='level9')
        l = tech_level.TechLevel()
        t.level.biotechnology = 9
        s.set_hull(tech.Tech(ID='hull1', slots_general=1))
        s.add_component(t)
        self.assertFalse(s.is_valid(level=l))

    def test_clone(self):
        s1 = ship_design.ShipDesign()
        s1.add_component(tech.Tech(ID='a123', armor=123))
        s1.add_component(tech.Tech(ID='a321', armor=321))
        s2 = s1.clone_design()
        self.assertEqual(s2.armor, 444)
        self.assertNotEqual(s1.ID, s2.ID)
