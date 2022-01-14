import unittest
from .. import *

class BuildShipTestCase(unittest.TestCase):
    def test_build1(self):
        p = planet.Planet()
        b = build_ship.BuildShip(planet=reference.Reference(p))
        t1 = tech.Tech()
        t1.cost.energy = 800
        b.buships.ship_design.add_component(t1)
        c = b.build(cost.Cost(energy=23))
        self.assertEqual(c.energy, 538)
        c = b.build(c)
        self.assertEqual(c.energy, 0)

    def test_build2(self):
        p = planet.Planet()
        b = build_ship.BuildShip(planet=reference.Reference(p))
        t1 = tech.Tech()
        t1.cost.energy = 23
        t2 = tech.Tech()
        t2.cost.energy = 800
        b.buships.ship_design.add_component(t1)
        b.buships.ship_design.add_component(t2)
        p.player.add_ships(b.buships)
        c = b.build(cost.Cost(energy=23))
        self.assertTrue(b.ship.under_construction)
        c = b.build(cost.Cost(energy=30))
        c = b.build(cost.Cost(energy=30))
        self.assertEqual(c.energy, 501)
        c = b.build(cost.Cost(energy=501))
        self.assertFalse(b.ship.under_construction)

    def test_build3(self):
        p = planet.Planet()
        p.player.tech_level.weapons = 10
        b = build_ship.BuildShip(planet=reference.Reference(p))
        h = tech.Tech(slots_general=1)
        h.cost.energy = 100
        h.cost.titanium = 100
        b.buships.ship_design.add_component(h)
        t1 = tech.Tech()
        t1.cost.energy = 100
        t1.cost.titanium = 100
        b.ship = reference.Reference(ship.Ship())
        b.ship.add_component(h)
        b.ship.add_component(t1)
        b.ship.update()
        c = b.build()
        self.assertEqual(c.energy, 49)
        c = b.build(c)
        self.assertEqual(c.energy, 0)

    def test_update_cost1(self):
        p = planet.Planet()
        p.player.tech_level.weapons = 10
        b = build_ship.BuildShip(planet=reference.Reference(p))
        h = tech.Tech(slots_general=1)
        c = tech.Tech()
        c.cost.energy = 100
        c.level.weapons = 5
        b.buships.ship_design.add_component(c)
        b.buships.ship_design.add_component(h)
        b._update_cost()
        self.assertEqual(b.level.weapons, 10)
        self.assertEqual(b.to_build[0].ID, h.ID)
        self.assertEqual(b.to_build[1].ID, c.ID)
        self.assertEqual(len(b.to_scrap), 0)
        self.assertTrue(b.scrap_minerals.is_zero())
        self.assertTrue(b.overhaul.is_zero())
        self.assertEqual(b.cost.energy, 81)

    def test_update_cost2(self):
        p = planet.Planet()
        p.player.tech_level.weapons = 10
        b = build_ship.BuildShip(planet=reference.Reference(p))
        h = tech.Tech(slots_general=1)
        h.cost.energy = 100
        h.cost.titanium = 100
        c = tech.Tech()
        c.cost.energy = 100
        c.level.weapons = 5
        b.buships.ship_design.add_component(c)
        b.buships.ship_design.add_component(h)
        b.ship = reference.Reference(ship.Ship())
        b.ship.add_component(h)
        b.ship.update()
        b._update_cost()
        self.assertEqual(b.level.weapons, 10)
        self.assertEqual(b.to_build[0].ID, c.ID)
        self.assertEqual(len(b.to_scrap), 0)
        self.assertTrue(b.scrap_minerals.is_zero())
        self.assertEqual(b.overhaul.energy, 49)
        self.assertEqual(round(b.overhaul.titanium), 50)
        self.assertEqual(b.cost.energy, 130)

    def test_update_cost3(self):
        p = planet.Planet()
        p.player.tech_level.weapons = 10
        b = build_ship.BuildShip(planet=reference.Reference(p))
        h = tech.Tech(slots_general=1)
        c = tech.Tech()
        c.cost.titanium = 100
        c.level.weapons = 5
        b.buships.ship_design.add_component(h)
        b.buships.overhaul = False
        b.ship = reference.Reference(ship.Ship())
        b.ship.add_component(c)
        b.ship.update()
        b._update_cost()
        self.assertEqual(b.level.weapons, 0)
        self.assertEqual(b.to_build[0].ID, h.ID)
        self.assertEqual(b.to_scrap[0].ID, c.ID)
        self.assertEqual(b.scrap_minerals.titanium, 50)
        self.assertTrue(b.overhaul.is_zero())
        self.assertEqual(b.cost.energy, 0)
