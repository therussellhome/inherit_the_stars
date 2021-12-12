import unittest
from unittest.mock import patch
from .. import *

class ShipTestCase(unittest.TestCase):
    def test_init1(self):
        s1 = ship.Ship(armor=321)
        s2 = ship.Ship(armor=456)
        s0 = ship.Ship(from_ships=[s1, s2])
        self.assertEqual(s0.armor, 777)

    def test_attribute1(self):
        s = ship.Ship(battle_experience=1.2, navigation_experience=3.4)
        self.assertEqual(s.initiative, 5.6)

    def test_attribute2(self):
        s = ship.Ship(mass=100)
        s.cargo.titanium = 100
        self.assertEqual(s.total_mass, 200)

    def test_attribute3(self):
        s = ship.Ship(mass=100)
        s.cargo.titanium = 100
        s.cargo.people = 10
        s.crew.lrt_Trader = True
        self.assertEqual(s.apparent_mass, 110)

    def test_attribute4(self):
        s = ship.Ship(mass=100)
        s.cargo.titanium = 100
        s.crew.primary_race_trait = 'Kender'
        self.assertEqual(s.apparent_mass, 175)

    def test_attribute5(self):
        s = ship.Ship(mass=100)
        s.engines.append('')
        s.engines.append('')
        s.cargo.titanium = 100
        self.assertEqual(s.mass_per_engine, 100)

    def test_hundreth1(self):
        s = ship.Ship(ke=100)
        s.next_hundreth()
        self.assertEqual(s.ke, 0)

    def test_updatecargo1(self):
        s = ship.Ship(total_mass=100)
        s.update_cargo()
        self.assertEqual(s.total_mass, 0)

    def test_damage1(self):
        s = ship.Ship(armor=100)
        s.take_damage(25, 75)
        self.assertEqual(s['shield_damage'], 25)
        self.assertEqual(s['armor_damage'], 75)

    def test_damage2(self):
        s = ship.Ship(armor=100)
        s.fleet = fleet.Fleet() + s
        with patch.object(player.Player, 'remove_ships') as mock:
            s.take_damage(25, 175)
            self.assertEqual(mock.call_count, 1)

    def test_scrap1(self):
        s = ship.Ship()
        s.cargo.titanium = 100
        self.assertEqual(s.scrap(10).titanium, 90)

    def test_scrap2(self):
        s = ship.Ship()
        p = planet.Planet()
        s.location = location.Location(reference=p)
        s.cargo.titanium = 100
        s.scrap()
        self.assertEqual(p.on_surface.titanium, 100)

    def test_scan1(self):
        s = ship.Ship()
        self.assertTrue('Mass' in s.scan_report('anticloak'))

    def test_scan2(self):
        s = ship.Ship()
        self.assertTrue('Apparent Mass' in s.scan_report('penetrating'))

    def test_scan3(self):
        s = ship.Ship()
        self.assertTrue('Apparent KE' in s.scan_report('normal'))
