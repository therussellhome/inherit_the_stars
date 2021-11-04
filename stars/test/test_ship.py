import unittest
from unittest.mock import patch
from .. import *

class ShipTestCase(unittest.TestCase):
    def test_init1(self):
        s1 = ship.Ship(armor=321)
        s2 = ship.Ship(armor=456)
        s0 = ship.Ship(from_ships=[s1, s2])
        self.assertEqual(s0.armor, 777)

    def test_cache1(self):
        s = ship.Ship(mass=100)
        s.cargo.titanium = 100
        s.update_cache(reference.Reference('Player'), reference.Reference('Fleet'))
        self.assertEqual(s['apparent_mass'], 200)

    def test_cache2(self):
        s = ship.Ship(mass=100)
        s.crew.lrt_Trader = True
        s.cargo.titanium = 100
        s.update_cache(reference.Reference('Player'), reference.Reference('Fleet'))
        self.assertEqual(s['apparent_mass'], 100)

    def test_cache3(self):
        s = ship.Ship(mass=100)
        s.crew.primary_race_trait = 'Kender'
        s.cargo.titanium = 100
        s.update_cache(reference.Reference('Player'), reference.Reference('Fleet'))
        self.assertEqual(s['apparent_mass'], 175)

    def test_cache3(self):
        s = ship.Ship(mass=100)
        s.engines.append('')
        s.engines.append('')
        s.cargo.titanium = 100
        s.update_cache(reference.Reference('Player'), reference.Reference('Fleet'))
        self.assertEqual(s['mass_per_engine'], 100)

    def test_damage1(self):
        s = ship.Ship(armor=100)
        s.take_damage(25, 75)
        self.assertEqual(s['shield_damage'], 25)
        self.assertEqual(s['armor_damage'], 75)

    def test_damage2(self):
        s = ship.Ship(armor=100)
        s.update_cache(reference.Reference('Player'), fleet.Fleet)
        with patch.object(player.Player, 'remove_ships') as mock:
            s.take_damage(25, 175)
            self.assertEqual(mock.call_count, 1)
