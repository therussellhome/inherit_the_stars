import unittest
from .. import *

class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.planet = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        self.planet.colonize(reference.Reference('Player', 'test_planet'), 'default', 25000, 1)

    def test_colonize(self):
        self.planet.colonize(reference.Reference('Player', 'test_colonize'), 'default', 25000, 1)
        self.assertEqual(self.planet.on_surface.people, 25000)
        self.assertEqual(self.planet.factories, 2)

    def test_calculate_effort(self):
        self.planet.on_surface.people = 1000
        self.assertEqual(self.planet._calc_effort(), 1000000)
        self.planet.on_surface.people = 500
        self.assertEqual(self.planet._calc_effort(), 500000)
        self.planet.on_surface.people = 1000
        self.planet.player.race.effort_per_kt = 800
        self.assertEqual(self.planet._calc_effort(), 800000)

    def test_generate_energy(self):
        # TODO
        pass

    def test_calc_max_production_capacity(self):
        # TODO
        pass

    def test_mine_minerals(self):
        # TODO
        pass

    def test_calc_planet_value(self):
        self.__calcplanet_value_expect(50, 50, 50, 0, 100, 0, 100, 0, 100, 100)
        self.__calcplanet_value_expect(0, 50, 50, 0, 100, 0, 100, 0, 100, 41)
        self.__calcplanet_value_expect(0, -15, 50, 0, 100, 0, 100, 0, 100, -9) 
        self.__calcplanet_value_expect(4, 114, 12, 0, 100, 0, 100, 0, 100, -8) 
        self.__calcplanet_value_expect(100, -12, 0, 0, 100, 110, 114, 0, 100, -59)
        self.__calcplanet_value_expect(0, 115, 100, 99, 100, -1, -15, 0, 12, -100)
        self.__calcplanet_value_expect(99, 1, 6, 98, 100, -1, -15, 0, 12, -59)
        self.__calcplanet_value_expect(30, 30, 30, 0, 100, 0, 100, 0, 100, 60)
        self.__calcplanet_value_expect(30, 90, 60, 0, 100, 0, 100, 0, 100, 41)
        self.__calcplanet_value_expect(18, 1, 40, 0, 100, 0, 100, 0, 100, 23) 
        self.__calcplanet_value_expect(300, 2000, 'me', 0, 100, 0, 100, 0, 100, -9)
        self.__calcplanet_value_expect(150, 304, 30, -900, 100, 0, -8000, 0, 100, -59)
        self.__calcplanet_value_expect(-30, 30, -0, 0, 10, 0, 00, 0, 360, -59)
        self.__calcplanet_value_expect(950, 3300, -430, 0, 100, 0, 1010, 'break', 100, -9)
        self.__calcplanet_value_expect(70, 33, -430, 0, 100, 0, 68, 90, 100, -59)
        self.__calcplanet_value_expect(950, 60, 70, 70, 100, 70, 100, 70, 100, -30)

    def __calcplanet_value_expect(self, g, t, r, g_start, g_stop, t_start, t_stop, r_start, r_stop, expect):
        self.planet.gravity = g
        self.planet.temperature = t
        self.planet.radiation = r
        race = self.planet.player.race
        race.gravity_start = g_start
        race.gravity_stop = g_stop
        race.temperature_start = t_start
        race.temperature_stop = t_stop
        race.radiation_start = r_start
        race.radiation_stop = r_stop
        self.assertEqual(self.planet.calc_planet_value(race), expect)

    def test_have_babies(self):
        self.planet.player.race.growth_rate = 10
        self.planet.player.race.maximum_population = 10000000
        self.planet.on_surface.people = 250
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 225)
        self.planet.player.race.growth_rate = 10
        self.planet.on_surface.people = 0
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 0)
        self.planet.player.race.growth_rate = 10
        self.planet.on_surface.people = -10
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 0)
        self.planet.player.race.growth_rate = 0
        self.planet.on_surface.people = 250
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 250)
        self.planet.player.race.growth_rate = -10
        self.planet.on_surface.people = 250
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 250)
        self.planet.player.race.growth_rate = -10
        self.planet.on_surface.people = 'me'
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 0)
        self.planet.player.race.growth_rate = 'chicken'
        self.planet.on_surface.people = 250
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 225)
        self.planet.planet_value = -100
        self.planet.player.race.growth_rate = -10
        self.planet.on_surface.people = 250
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 250)
        self.planet.player.race.growth_rate = 10
        self.planet.on_surface.people = 250
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 225)
        self.planet.planet_value = 100
        self.planet.player.race.growth_rate = -20
        self.planet.on_surface.people = 220
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 220)
        self.planet.planet_value = 0
        self.planet.player.race.growth_rate = 10
        self.planet.on_surface.people = 250
        self.planet.have_babies()
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 202)
        self.planet.player.race.growth_rate = 20
        self.planet.planet_value = 100
        self.planet.on_surface.people = 100
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 120)
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 144)
        self.planet.player.race.growth_rate = 20
        self.planet.on_surface.people = 10000
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 10000)
        self.planet.on_surface.people = 9999
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 10000)
    
    def test_auto_build(self):
        self.planet = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        self.planet.colonize(reference.Reference('Player', 'test_planet'), 'default', 25, 1)
        self.planet.minister = reference.Reference('Minister', 'test_Minister')
        self.planet.mines = 25
        self.planet.power_plants = 3
        self.planet.factories = 2
        self.planet.defenses = 4
        self.assertEqual(self.planet.auto_build(), self.planet.factory_tech)
        self.planet.mines = 25
        self.planet.power_plants = 50
        self.planet.factories = 2
        self.planet.defenses = 4
        self.assertEqual(self.planet.auto_build(), self.planet.scanner_tech)
        self.planet.mines = 25
        self.planet.power_plants = 47
        self.planet.factories = 25
        self.planet.defenses = 4
        self.assertEqual(self.planet.auto_build(), self.planet.penetrating_tech)
        self.planet.mines = 2
        self.planet.power_plants = 5
        self.planet.factories = 2
        self.planet.defenses = 1
        self.assertEqual(self.planet.auto_build(), self.planet.defense_tech)
        self.planet.mines = 5
        self.planet.power_plants = 3
        self.planet.factories = 22
        self.planet.defenses = 4
        self.assertEqual(self.planet.auto_build(), self.planet.power_plant_tech)
        self.planet.mines = 2
        self.planet.power_plants = 3
        self.planet.factories = 26
        self.planet.defenses = 4
        self.assertEqual(self.planet.auto_build(), self.planet.mine_tech)
        
