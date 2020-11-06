import unittest
from .. import *
from colorsys import hls_to_rgb

class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.planet = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        self.planet.colonize(reference.Reference('Player', 'test_planet'), 'New Colony Minister')

    def test_orbit(self):
        return #TODO orbit not finished
        self.planet.age = 2097
        self.assertEqual(self.planet.orbit(), )
        
    def test_get_color(self):
        self.planet.radiation = 100
        self.planet.temperature = -50
        self.assertEqual(self.planet.get_color(), '#FF0000')
        self.planet.temperature = 150
        self.assertEqual(self.planet.get_color(), '#7F00FF')
        self.planet.radiation = 0
        self.assertEqual(self.planet.get_color(), '#7F40BF')
        self.planet.radiation = 50
        self.assertEqual(self.planet.get_color(), '#7F20DF')
        self.planet.temperature = 75
        self.assertEqual(self.planet.get_color(), '#2097DF')
        self.planet.radiation = 100
        self.assertEqual(self.planet.get_color(), '#009FFF')
        #reset gravity, temperature and radiation so other functions don't have problems
        self.planet.gravity = 50
        self.planet.temperature = 50
        self.planet.radiation = 50
        self.assertEqual(self.planet.get_color(), '#20DF50')

    def test_generate_energy(self):
        play = player.Player(
            name = 'test_colonize',
            race = race.Race(
                scrap_rate = 90,
                colonists_to_operate_power_plant = 100,
                ),
            energy = 0,
            )
        self.planet.colonize(reference.Reference(play), 'New Colony Minister')
        self.planet.on_surface.people = 40
        self.planet.facilities['Power'].quantity = 100
        self.planet.facilities['Power'].tech.energy_output = 200
        self.planet.generate_energy()
        self.planet = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        self.planet.colonize(reference.Reference('Player', 'test_planet'), 'New Colony Minister')
        self.assertEqual(play.energy, 10000, 'FIX ME')
    
    def test_calc_max_production_capacity(self):
        play = player.Player(
            name = 'test_colonize',
            race = race.Race(
                scrap_rate = 90,
                colonists_to_operate_factory = 100,
                ),
            )
        self.planet.colonize(reference.Reference(play), 'New Colony Minister')
        self.planet.on_surface.people = 40
        self.planet.facilities['Power'].quantity = 100
        self.planet.facilities['Power'].tech.factory_capacity = 00
        self.planet.calc_production()
        self.assertEqual(self.planet.factory_capacity, 100, 'FIX ME')
        self.planet = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        self.planet.colonize(reference.Reference('Player', 'test_planet'), 'New Colony Minister')
        

    def test_mine_minerals(self):
        play = player.Player(
            name = 'test_colonize',
            race = race.Race(
                scrap_rate = 90,
                colonists_to_operate_mine = 100,
                ),
            energy = 0,
            )
        self.planet.colonize(reference.Reference(play), 'New Colony Minister')
        self.planet.on_surface = cargo.Cargo(people = 40)
        self.planet.remaining_minerals = minerals.Minerals(titanium=10000, silicon=10000, lithium=10000)
        self.planet.facilities['Mine'].quantity = 100
        self.planet.facilities['Mine'].tech.mineral_depletion_factor = 1.3
        self.planet._mine_minerals()
        self.assertEqual(self.planet.on_surface.titanium, 7, 'FIX ME')
        self.assertEqual(self.planet.on_surface.lithium, 7, 'FIX ME')
        self.assertEqual(self.planet.on_surface.silicon, 7, 'FIX ME')
        self.assertEqual(self.planet.remaining_minerals.titanium, 9993, 'FIX ME')
        self.assertEqual(self.planet.remaining_minerals.lithium, 9993, 'FIX ME')
        self.assertEqual(self.planet.remaining_minerals.silicon, 9993, 'FIX ME')
        self.planet = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        self.planet.colonize(reference.Reference('Player', 'test_planet'), 'New Colony Minister')

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
        self.__calcplanet_value_expect(300, 2000, 'me', 0, 100, 0, 100, 0, 100, -86)
        self.__calcplanet_value_expect(150, 304, 30, -900, 100, 0, -8000, 0, 100, -86)
        self.__calcplanet_value_expect(-30, 30, -0, 0, 10, 0, 00, 0, 360, -86)
        self.__calcplanet_value_expect(950, 3300, -430, 0, 100, 0, 1010, 'break', 100, -100)
        self.__calcplanet_value_expect(70, 33, -430, 0, 100, 0, 68, 90, 100, -59)
        self.__calcplanet_value_expect(950, 60, 70, 70, 100, 70, 100, 70, 100, -75)
        self.__calcplanet_value_expect(50, 50, 50, 50, 50, 50, 50, 50, 50, 100)
        

    def __calcplanet_value_expect(self, g, t, r, g_start, g_stop, t_start, t_stop, r_start, r_stop, expect):
        self.planet.gravity = g
        self.planet.temperature = t
        self.planet.radiation = r
        race = self.planet.player.race
        race.hab_gravity = g_start
        race.hab_gravity_stop = g_stop
        race.hab_temperature = t_start
        race.hab_temperature_stop = t_stop
        race.hab_radiation = r_start
        race.hab_radiation_stop = r_stop
        self.assertEqual(self.planet.calc_planet_value(race), expect)

    def test_have_babies(self):
        self.planet = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        self.planet.have_babies()
        self.planet.colonize(reference.Reference('Player', 'test_planet'), 'New Colony Minister')
        self.__calcplanet_value_expect(50, 50, 50, 0, 100, 0, 100, 0, 100, 100)
        self.planet.player.race.growth_rate = 10
        self.planet.player.race.maximum_population = 10000000
        self.planet.on_surface.people = 250
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 274)
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
        self.assertEqual(self.planet.on_surface.people, 252)
        self.__calcplanet_value_expect(0, 115, 100, 99, 100, -1, -15, 0, 12, -100)
        self.planet.player.race.growth_rate = 10
        self.planet.on_surface.people = 250
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 226)
        self.__calcplanet_value_expect(0, 0, 0, 0, 100, 0, 100, 0, 100, 0)
        self.planet.player.race.growth_rate = 10
        self.planet.on_surface.people = 250
        self.planet.have_babies()
        self.planet.have_babies()
        self.assertEqual(self.planet.on_surface.people, 250)
        self.__calcplanet_value_expect(50, 50, 50, 0, 100, 0, 100, 0, 100, 100)
        self.planet.player.race.growth_rate = 20
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
        self.assertEqual(self.planet.on_surface.people, 9999)
    
    def test_auto_build(self):
        self.planet.on_surface.people = 1000
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
        self.planet.mines = 25
        self.planet.power_plants = 3
        self.planet.factories = 2
        self.planet.defenses = 4
        #self.planet.auto_build().debug_display()
        #self.planet.facilities['Factory'].debug_display()
        self.assertEqual(self.planet.auto_build() is self.planet.facilities['Factory'], True, 'This error does not seem logical')#'FIX ME'
        self.planet.mines = 2
        self.planet.power_plants = 5
        self.planet.factories = 2
        self.planet.defenses = 1
        #self.planet.auto_build().debug_display()
        #self.planet.facilities['Defense'].debug_display()
        #self.assertEqual(self.planet.auto_build(), self.planet.facilities['Defense'], 'FIX ME')
        self.planet.mines = 5
        self.planet.power_plants = 3
        self.planet.factories = 22
        self.planet.defenses = 4
        #self.planet.auto_build().debug_display()
        #self.planet.facilities['Power'].debug_display()
        #self.assertEqual(self.planet.auto_build(), self.planet.facilities['Power'], 'FIX ME')
        self.planet.mines = 2
        self.planet.power_plants = 3
        self.planet.factories = 26
        self.planet.defenses = 4
        #self.planet.auto_build().debug_display()
        #self.planet.facilities['Mine'].debug_display()
        #self.assertEqual(self.planet.auto_build(), self.planet.facilities['Mine'], 'FIX ME')
        ###reset###
        self.planet = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        self.planet.colonize(reference.Reference('Player', 'test_planet'), 'New Colony Minister')
        
