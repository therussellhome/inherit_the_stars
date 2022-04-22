import unittest
from .. import *

class ShipDesignTestCase(unittest.TestCase):
    def test_add1(self):
        s = ship_design.ShipDesign()
        a321 = reference.Reference(tech.Tech(ID='a321', armor=321))
        s.add_component(a321)
        self.assertEqual(len(s.components.keys()), 1)
        self.assertEqual(s.components[a321], 1)

    def test_add2(self):
        s = ship_design.ShipDesign()
        a321 = reference.Reference(tech.Tech(ID='a321', armor=321))
        s.add_component(a321)
        s.add_component(a321)
        self.assertEqual(len(s.components.keys()), 1)
        self.assertEqual(s.components[a321], 2)

    def test_add3(self):
        s = ship_design.ShipDesign()
        hull = reference.Reference(tech.Tech(ID='hull', slots_general=2))
        s.add_component(hull)
        self.assertEqual(len(s.components.keys()), 1)
        self.assertEqual(s.components[hull], 1)

    def test_add4(self):
        s = ship_design.ShipDesign()
        hull = reference.Reference(tech.Tech(ID='hull', slots_general=2))
        s.add_component(hull)
        s.add_component(hull)
        self.assertEqual(len(s.components.keys()), 1)
        self.assertEqual(s.components[hull], 1)

    def test_add5(self):
        s = ship_design.ShipDesign()
        hull = reference.Reference(tech.Tech(ID='hull', slots_general=2))
        hull2 = reference.Reference(tech.Tech(ID='hull2', slots_general=1))
        s.add_component(hull)
        s.add_component(hull2)
        self.assertEqual(len(s.components.keys()), 1)
        self.assertEqual(s.components[hull2], 1)

    def test_rm1(self):
        s = ship_design.ShipDesign()
        a321 = reference.Reference(tech.Tech(ID='a321', armor=321))
        s.add_component(a321)
        s.add_component(a321)
        s.remove_component(a321)
        self.assertEqual(len(s.components.keys()), 1)
        self.assertEqual(s.components[a321], 1)

    def test_rm2(self):
        s = ship_design.ShipDesign()
        a321 = reference.Reference(tech.Tech(ID='a321', armor=321))
        s.add_component(a321)
        s.remove_component(a321)
        self.assertEqual(len(s.components.keys()), 0)

    def test_update1(self):
        s = ship_design.ShipDesign()
        a456 = reference.Reference(tech.Tech(ID='a456', armor=456))
        a321 = reference.Reference(tech.Tech(ID='a321', armor=321))
        s.armor = 999
        s.add_component(a456)
        s.add_component(a321)
        s.update()
        self.assertEqual(s.armor, 777)

    def test_valid1(self):
        s = ship_design.ShipDesign()
        a456 = reference.Reference(tech.Tech(ID='a456', armor=456))
        a321 = reference.Reference(tech.Tech(ID='a321', armor=321))
        s.add_component(a456)
        s.add_component(a321)
        s.update()
        self.assertFalse(s.is_valid())

    def test_valid2(self):
        s = ship_design.ShipDesign()
        hull = reference.Reference(tech.Tech(ID='hull', slots_general=2))
        a456 = reference.Reference(tech.Tech(ID='a456', armor=456))
        a321 = reference.Reference(tech.Tech(ID='a321', armor=321))
        s.add_component(hull)
        s.add_component(a456)
        s.add_component(a321)
        s.update()
        self.assertTrue(s.is_valid())

    def test_valid3(self):
        s = ship_design.ShipDesign()
        hull = reference.Reference(tech.Tech(ID='hull', slots_general=2))
        a456 = reference.Reference(tech.Tech(ID='a456', armor=456))
        a321 = reference.Reference(tech.Tech(ID='a321', armor=321))
        s.add_component(hull)
        s.add_component(a456)
        s.add_component(a321)
        s.components[hull] = 2
        s.update()
        self.assertFalse(s.is_valid())

    def test_valid4(self):
        s = ship_design.ShipDesign()
        hull3 = reference.Reference(tech.Tech(ID='hull3', slots_general=2, level=tech_level.TechLevel(energy=10)))
        a456 = reference.Reference(tech.Tech(ID='a456', armor=456))
        a321 = reference.Reference(tech.Tech(ID='a321', armor=321))
        s.add_component(hull3)
        s.add_component(a456)
        s.add_component(a321)
        s.update()
        self.assertFalse(s.is_valid(level=tech_level.TechLevel()))

    def test_hull1(self):
        s = ship_design.ShipDesign()
        hull = reference.Reference(tech.Tech(ID='hull', slots_general=2))
        s.add_component(hull)
        self.assertEqual(s.hull(), hull)

    def test_hull2(self):
        s = ship_design.ShipDesign()
        self.assertEqual(s.hull().slots_general, -1)

    def test_spacestation1(self):
        s = ship_design.ShipDesign()
        hull = reference.Reference(tech.Tech(ID='hull', slots_general=2))
        s.add_component(hull)
        self.assertFalse(s.is_space_station())

    def test_clone(self):
        s1 = ship_design.ShipDesign()
        s1.add_component(tech.Tech(ID='a123', armor=123))
        s1.add_component(tech.Tech(ID='a321', armor=321))
        s1.update()
        s2 = s1.clone_design()
        s2.update()
        self.assertEqual(s2.armor, 444)
        self.assertNotEqual(s1.ID, s2.ID)
