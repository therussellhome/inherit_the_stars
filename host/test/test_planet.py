import unittest
from .. import *

class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.planet = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        self.planet.colonize(25000, game_engine.Reference('Player', 'test_planet'))

    def test_calc_planet_value(self):
        self._test_calc_planet_value_expect(50, 50, 50, 0, 100, 0, 100, 0, 100, 100)
        self._test_calc_planet_value_expect(0, 50, 50, 0, 100, 0, 100, 0, 100, 41)
        self._test_calc_planet_value_expect(0, -15, 50, 0, 100, 0, 100, 0, 100, -9) 
        self._test_calc_planet_value_expect(4, 114, 12, 0, 100, 0, 100, 0, 100, -8) 
        self._test_calc_planet_value_expect(100, -12, 0, 0, 100, 110, 114, 0, 100, -59)
        self._test_calc_planet_value_expect(0, 115, 100, 99, 100, -1, -15, 0, 12, -100)
        self._test_calc_planet_value_expect(99, 1, 6, 98, 100, -1, -15, 0, 12, -59)
        self._test_calc_planet_value_expect(30, 30, 30, 0, 100, 0, 100, 0, 100, 60)
        self._test_calc_planet_value_expect(30, 90, 60, 0, 100, 0, 100, 0, 100, 41)
        self._test_calc_planet_value_expect(18, 1, 40, 0, 100, 0, 100, 0, 100, 23) 
        self._test_calc_planet_value_expect(300, 2000, 'me', 0, 100, 0, 100, 0, 100, -9)
        self._test_calc_planet_value_expect(150, 304, 30, -900, 100, 0, -8000, 0, 100, -59)
        self._test_calc_planet_value_expect(-30, 30, -0, 0, 10, 0, 00, 0, 360, -59)
        self._test_calc_planet_value_expect(950, 3300, -430, 0, 100, 0, 1010, 'break', 100, -9)
        self._test_calc_planet_value_expect(70, 33, -430, 0, 100, 0, 68, 90, 100, -59)
        self._test_calc_planet_value_expect(950, 60, 70, 70, 100, 70, 100, 70, 100, -30)

    def _test_calc_planet_value_expect(self, g, t, r, g_start, g_stop, t_start, t_stop, r_start, r_stop, expect):
        self.planet.gravity = g
        self.planet.temperature = t
        self.planet.radiation = r
        self.planet.player.race.gravity_start = g_start
        self.planet.player.race.gravity_stop = g_stop
        self.planet.player.race.temperature_start = t_start
        self.planet.player.race.temperature_stop = t_stop
        self.planet.player.race.radiation_start = r_start
        self.planet.player.race.radiation_stop = r_stop
        self.assertEqual(self.planet._calc_planet_value(), expect)

    def test_grow_population(self):
        self.planet.player.race.growth_rate = 10
        self.planet.player.race.maximum_population = 10000000
        self.planet.on_surface.people = 250
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 225)
        self.planet.player.race.growth_rate = 10
        self.planet.on_surface.people = 0
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 0)
        self.planet.player.race.growth_rate = 10
        self.planet.on_surface.people = -10
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 0)
        self.planet.player.race.growth_rate = 0
        self.planet.on_surface.people = 250
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 250)
        self.planet.player.race.growth_rate = -10
        self.planet.on_surface.people = 250
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 250)
        self.planet.player.race.growth_rate = -10
        self.planet.on_surface.people = 'me'
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 0)
        self.planet.player.race.growth_rate = 'chicken'
        self.planet.on_surface.people = 250
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 225)
        self.planet.planet_value = -100
        self.planet.player.race.growth_rate = -10
        self.planet.on_surface.people = 250
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 250)
        self.planet.player.race.growth_rate = 10
        self.planet.on_surface.people = 250
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 225)
        self.planet.planet_value = 100
        self.planet.player.race.growth_rate = -20
        self.planet.on_surface.people = 220
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 220)
        self.planet.planet_value = 0
        self.planet.player.race.growth_rate = 10
        self.planet.on_surface.people = 250
        self.planet._grow_population()
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 202)
        self.planet.player.race.growth_rate = 20
        self.planet.planet_value = 100
        self.planet.on_surface.people = 100
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 120)
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 144)
        self.planet.player.race.growth_rate = 20
        self.planet.on_surface.people = 10000
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 10000)
        self.planet.on_surface.people = 9999
        self.planet._grow_population()
        self.assertEqual(self.planet.on_surface.people, 10000)
    
    def test_auto_build(self):
        self.planet = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        self.planet.colonize(25, game_engine.Reference('Player', 'test_planet'))
        self.planet.minister = game_engine.Reference('Minister', 'test_Minister')
        self.planet.mines = 25
        self.planet.power_plants = 3
        self.planet.factories = 2
        self.planet.defenses = 4
        self.assertEqual(self.planet._check_should_build_facility(), 'self.factory_tech')
        self.planet.mines = 25
        self.planet.power_plants = 50
        self.planet.factories = 2
        self.planet.defenses = 4
        self.assertEqual(self.planet._check_should_build_facility(), 'self.scanner_tech')
        self.planet.mines = 25
        self.planet.power_plants = 47
        self.planet.factories = 25
        self.planet.defenses = 4
        self.assertEqual(self.planet._check_should_build_facility(), 'self.penetrating_tech')
        self.planet.mines = 2
        self.planet.power_plants = 5
        self.planet.factories = 2
        self.planet.defenses = 1
        self.assertEqual(self.planet._check_should_build_facility(), 'self.defense_tech')
        self.planet.mines = 5
        self.planet.power_plants = 3
        self.planet.factories = 22
        self.planet.defenses = 4
        self.assertEqual(self.planet._check_should_build_facility(), 'self.power_plant_tech')
        self.planet.mines = 2
        self.planet.power_plants = 3
        self.planet.factories = 26
        self.planet.defenses = 4
        self.assertEqual(self.planet._check_should_build_facility(), 'self.mine_tech')
        
