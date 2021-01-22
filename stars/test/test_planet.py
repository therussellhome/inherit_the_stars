import unittest
import sys
from .. import *
from colorsys import hls_to_rgb

class PlanetTestCase(unittest.TestCase):


    def test_get_color1(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        self.assertEqual(p.get_color(), '#20DF50')

    def test_get_color2(self):
        p = planet.Planet(gravity=50, temperature=-50, radiation=100)
        self.assertEqual(p.get_color(), '#FF0000')

    def test_get_color3(self):
        p = planet.Planet(gravity=50, temperature=150, radiation=100)
        self.assertEqual(p.get_color(), '#7F00FF')

    def test_get_color4(self):
        p = planet.Planet(gravity=50, temperature=150, radiation=0)
        self.assertEqual(p.get_color(), '#7F40BF')

    def test_get_color5(self):
        p = planet.Planet(gravity=50, temperature=150, radiation=50)
        self.assertEqual(p.get_color(), '#7F20DF')

    def test_get_color6(self):
        p = planet.Planet(gravity=50, temperature=75, radiation=50)
        self.assertEqual(p.get_color(), '#2097DF')

    def test_get_color7(self):
        p = planet.Planet(gravity=50, temperature=75, radiation=100)
        self.assertEqual(p.get_color(), '#009FFF')


    def test_orbit(self):
        return #TODO orbit not finished
        p.age = 2097
        self.assertEqual(p.orbit(), )


    def test_is_colonized1(self):
        p = planet.Planet()
        self.assertFalse(p.is_colonized())

    def test_is_colonized2(self):
        p = planet.Planet()
        # force reference to create the player
        p.player.name = 'colonized'
        self.assertTrue(p.is_colonized())


    def test_colonize1(self):
        p = planet.Planet()
        self.assertTrue(p.colonize(player.Player(name='test_colonize')))
        self.assertTrue(p.is_colonized())
        self.assertFalse(p.colonize(player.Player(name='claim jumper')))

    def test_colonize2(self):
        p = planet.Planet()
        p.colonize(player.Player(name='test_colonize'))
        self.assertFalse(p.colonize(player.Player(name='claim jumper')))

    def test_colonize3(self):
        p = planet.Planet()
        self.assertFalse(p.colonize(player.Player(race=race.Race(primary_race_trait='Pa\'anuri'))))


    def test_habitability1(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=100,
            hab_radiation=0, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), 100)

    def test_habitability2(self):
        p = planet.Planet(gravity=0, temperature=50, radiation=50)
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=100,
            hab_radiation=0, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), 41)

    def test_habitability3(self):
        p = planet.Planet(gravity=0, temperature=-15, radiation=50)
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=100,
            hab_radiation=0, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), -9)

    def test_habitability4(self):
        p = planet.Planet(gravity=4, temperature=114, radiation=12)
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=100,
            hab_radiation=0, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), -8)

    def test_habitability5(self):
        p = planet.Planet(gravity=100, temperature=-12, radiation=0)
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=110, hab_temperature_stop=114,
            hab_radiation=0, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), -59)

    def test_habitability6(self):
        p = planet.Planet(gravity=0, temperature=115, radiation=100)
        r = race.Race(hab_gravity=99, hab_gravity_stop=100,
            hab_temperature=-1, hab_temperature_stop=-15,
            hab_radiation=0, hab_radiation_stop=12)
        self.assertEqual(p.habitability(r), -100)

    def test_habitability7(self):
        p = planet.Planet(gravity=99, temperature=1, radiation=6)
        r = race.Race(hab_gravity=98, hab_gravity_stop=100,
            hab_temperature=-1, hab_temperature_stop=-15,
            hab_radiation=0, hab_radiation_stop=12)
        self.assertEqual(p.habitability(r), -59)

    def test_habitability8(self):
        p = planet.Planet(gravity=30, temperature=30, radiation=30)
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=100,
            hab_radiation=0, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), 60)

    def test_habitability9(self):
        p = planet.Planet(gravity=30, temperature=90, radiation=60)
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=100,
            hab_radiation=0, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), 41)

    def test_habitability10(self):
        p = planet.Planet(gravity=18, temperature=1, radiation=40)
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=100,
            hab_radiation=0, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), 23)

    def test_habitability11(self):
        p = planet.Planet(gravity=300, temperature=2000, radiation='me')
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=100,
            hab_radiation=0, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), -86)

    def test_habitability12(self):
        p = planet.Planet(gravity=150, temperature=304, radiation=30)
        r = race.Race(hab_gravity=-900, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=-8000,
            hab_radiation=0, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), -86)

    def test_habitability13(self):
        p = planet.Planet(gravity=-30, temperature=30, radiation=-0)
        r = race.Race(hab_gravity=0, hab_gravity_stop=10,
            hab_temperature=0, hab_temperature_stop=00,
            hab_radiation=0, hab_radiation_stop=360)
        self.assertEqual(p.habitability(r), -86)

    def test_habitability14(self):
        p = planet.Planet(gravity=950, temperature=3300, radiation=-430)
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=1010,
            hab_radiation='break', hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), -100)

    def test_habitability15(self):
        p = planet.Planet(gravity=70, temperature=33, radiation=-430)
        r = race.Race(hab_gravity=0, hab_gravity_stop=100,
            hab_temperature=0, hab_temperature_stop=68,
            hab_radiation=90, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), -59)

    def test_habitability16(self):
        p = planet.Planet(gravity=950, temperature=60, radiation=70)
        r = race.Race(hab_gravity=70, hab_gravity_stop=100,
            hab_temperature=70, hab_temperature_stop=100,
            hab_radiation=70, hab_radiation_stop=100)
        self.assertEqual(p.habitability(r), -75)

    def test_habitability17(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        r = race.Race(hab_gravity=50, hab_gravity_stop=50,
            hab_temperature=50, hab_temperature_stop=50,
            hab_radiation=50, hab_radiation_stop=50)
        self.assertEqual(p.habitability(r), 100)


    def test_growth_rate1(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        r = race.Race()
        self.assertEqual(p.growth_rate(r), 15)

    def test_growth_rate2(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        r = race.Race(growth_rate=10)
        self.assertEqual(p.growth_rate(r), 10)

    def test_growth_rate3(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        r = race.Race(hab_radiation=0, hab_radiation_stop=2, hab_gravity=0, hab_gravity_stop=2, hab_temperature=0, hab_temperature_stop=2)
        self.assertEqual(p.growth_rate(r), -15)


    def test_maxpop1(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        r = race.Race()
        self.assertEqual(p.maxpop(r), 10000000)

    def test_maxpop2(self):
        p = planet.Planet(gravity=100, temperature=50, radiation=50)
        r = race.Race()
        self.assertEqual(p.maxpop(r), 17500000)

    def test_maxpop3(self):
        p = planet.Planet(gravity=0, temperature=50, radiation=50)
        r = race.Race()
        self.assertEqual(p.maxpop(r), 2500000)

    def test_maxpop4(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        r = race.Race(body_mass=10)
        self.assertEqual(p.maxpop(r), 80000000)

    def test_maxpop5(self):
        p = planet.Planet(gravity=100, temperature=50, radiation=50)
        r = race.Race(body_mass=10)
        self.assertEqual(p.maxpop(r), 140000000)

    def test_maxpop6(self):
        p = planet.Planet(gravity=0, temperature=50, radiation=50)
        r = race.Race(body_mass=10)
        self.assertEqual(p.maxpop(r), 20000000)

    def test_maxpop7(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        r = race.Race(body_mass=150)
        self.assertEqual(p.maxpop(r), 5333333)

    def test_maxpop8(self):
        p = planet.Planet(gravity=100, temperature=50, radiation=50)
        r = race.Race(body_mass=150)
        self.assertEqual(p.maxpop(r), 9333333)

    def test_maxpop9(self):
        p = planet.Planet(gravity=0, temperature=50, radiation=50)
        r = race.Race(body_mass=150)
        self.assertEqual(p.maxpop(r), 1333333)


    def test_have_babies1(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        p.on_surface.people = 250
        for pop in [250.366, 250.732, 251.099, 251.466, 251.834, 252.202, 252.571, 252.940, 253.310, 253.680, 254.051, 254.422, 254.794, 255.166, 255.539, 255.913, 256.287, 256.662, 257.037, 257.413, 257.789, 258.166, 258.543, 258.921, 259.299, 259.678, 260.057, 260.437, 260.817, 261.198, 261.580, 261.962, 262.345, 262.728, 263.112, 263.496, 263.881, 264.266, 264.652, 265.038, 265.425, 265.813, 266.201, 266.590, 266.979, 267.369, 267.759, 268.150, 268.541, 268.933, 269.326, 269.719, 270.113, 270.507, 270.902, 271.297, 271.693, 272.089, 272.486, 272.884, 273.282, 273.681, 274.080, 274.480, 274.880, 275.281, 275.683, 276.085, 276.488, 276.891, 277.295, 277.699, 278.104, 278.510, 278.916, 279.323, 279.730, 280.138, 280.546, 280.955, 281.365, 281.775, 282.186, 282.597, 283.009, 283.421, 283.834, 284.248, 284.662, 285.077, 285.492, 285.908, 286.325, 286.742, 287.160, 287.578, 287.997, 288.417, 288.837, 289.258]:
            self.assertEqual(p.have_babies(), pop)

    def test_have_babies2(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        p.on_surface.people = 1
        for pop in [1.001, 1.003, 1.005, 1.007, 1.009, 1.011, 1.013, 1.015, 1.017, 1.019, 1.021, 1.023, 1.025, 1.027, 1.029, 1.031, 1.033, 1.035, 1.037, 1.039, 1.041, 1.043, 1.045, 1.047, 1.049, 1.051, 1.053, 1.055, 1.057, 1.059, 1.061, 1.063, 1.065, 1.067, 1.069, 1.071, 1.073, 1.075, 1.077, 1.079, 1.081, 1.083, 1.085, 1.087, 1.089, 1.091, 1.093, 1.095, 1.097, 1.099, 1.101, 1.103, 1.105, 1.107, 1.109, 1.111, 1.113, 1.115, 1.117, 1.119, 1.121, 1.123, 1.125, 1.127, 1.129, 1.131, 1.133, 1.135, 1.137, 1.139, 1.141, 1.143, 1.145, 1.147, 1.149, 1.151, 1.153, 1.155, 1.157, 1.159, 1.161, 1.163, 1.165, 1.167, 1.169, 1.171, 1.173, 1.175, 1.177, 1.179, 1.181, 1.183, 1.185, 1.187, 1.189, 1.191, 1.193, 1.195, 1.197, 1.199]:
            self.assertEqual(p.have_babies(), pop)

    def test_have_babies3(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        p.on_surface.people = 0
        self.assertEqual(p.have_babies(), 0)

    def test_have_babies4(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        p.player.race = race.Race(hab_radiation=0, hab_radiation_stop=2, hab_gravity=0, hab_gravity_stop=2, hab_temperature=0, hab_temperature_stop=2)
        p.on_surface.people = 250
        for pop in [249.634, 249.269, 248.904, 248.540, 248.176, 247.813, 247.450, 247.088, 246.727, 246.366, 246.006, 245.646, 245.287, 244.928, 244.570, 244.212, 243.855, 243.498, 243.142, 242.786, 242.431, 242.076, 241.722, 241.368, 241.015, 240.662, 240.310, 239.958, 239.607, 239.256, 238.906, 238.556, 238.207, 237.858, 237.510, 237.162, 236.815, 236.468, 236.122, 235.776, 235.431, 235.086, 234.742, 234.398, 234.055, 233.712, 233.370, 233.028, 232.687, 232.346, 232.006, 231.666, 231.327, 230.988, 230.650, 230.312, 229.974, 229.637, 229.300, 228.964, 228.628, 228.293, 227.958, 227.624, 227.290, 226.957, 226.624, 226.292, 225.960, 225.629, 225.298, 224.968, 224.638, 224.309, 223.980, 223.652, 223.324, 222.996, 222.669, 222.342, 222.016, 221.690, 221.365, 221.040, 220.716, 220.392, 220.069, 219.746, 219.424, 219.102, 218.781, 218.460, 218.139, 217.819, 217.499, 217.180, 216.861, 216.543, 216.225, 215.908]:
            self.assertEqual(p.have_babies(), pop)

    def test_have_babies5(self):
        p = planet.Planet(gravity=50, temperature=50, radiation=50)
        p.on_surface.people = 11000
        for pop in [10998.350, 10996.703, 10995.059, 10993.418, 10991.780, 10990.145, 10988.513, 10986.884, 10985.258, 10983.635, 10982.014, 10980.396, 10978.781, 10977.169, 10975.560, 10973.954, 10972.351, 10970.751, 10969.154, 10967.559, 10965.967, 10964.378, 10962.792, 10961.209, 10959.629, 10958.051, 10956.476, 10954.904, 10953.335, 10951.769, 10950.205, 10948.644, 10947.086, 10945.531, 10943.979, 10942.429, 10940.882, 10939.338, 10937.797, 10936.258, 10934.722, 10933.189, 10931.659, 10930.131, 10928.606, 10927.084, 10925.564, 10924.047, 10922.533, 10921.022, 10919.513, 10918.007, 10916.504, 10915.003, 10913.505, 10912.010, 10910.517, 10909.027, 10907.540, 10906.055, 10904.573, 10903.093, 10901.616, 10900.142, 10898.670, 10897.201, 10895.734, 10894.270, 10892.809, 10891.350, 10889.894, 10888.440, 10886.989, 10885.541, 10884.095, 10882.652, 10881.211, 10879.773, 10878.337, 10876.904, 10875.473, 10874.045, 10872.619, 10871.196, 10869.775, 10868.357, 10866.941, 10865.528, 10864.117, 10862.709, 10861.303, 10859.900, 10858.499, 10857.101, 10855.705, 10854.312, 10852.921, 10851.532, 10850.146, 10848.762]:
            self.assertEqual(p.have_babies(), pop)


    def test_raise_shields1(self):
        p = planet.Planet()
        p.on_surface.people = 1000 
        p.player.race.primary_race_trait = 'Gaerhule'
        p.player.tech_level.energy = 0
        p.defenses = 10
        self.assertEqual(p.raise_shields(), 4800)

    def test_raise_shields2(self):
        p = planet.Planet()
        p.on_surface.people = 1000 
        p.player.race.primary_race_trait = 'Gaerhule'
        p.player.tech_level.energy = 10
        p.defenses = 10
        self.assertEqual(p.raise_shields(), 24000)

    def test_raise_shields3(self):
        p = planet.Planet()
        p.on_surface.people = 1000 
        p.player.race.primary_race_trait = 'Patryns'
        p.player.tech_level.energy = 0
        p.defenses = 10
        self.assertEqual(p.raise_shields(), 2000)

    def test_raise_shields4(self):
        p = planet.Planet()
        p.on_surface.people = 1000 
        p.player.race.primary_race_trait = 'TANSTAAFL'
        p.player.tech_level.energy = 10
        p.defenses = 10
        self.assertEqual(p.raise_shields(), 20000)

    def test_raise_shields5(self):
        p = planet.Planet()
        p.on_surface.people = 1000 
        p.player.race.primary_race_trait = 'Aku\'Ultan'
        p.player.tech_level.energy = 30
        p.defenses = 16
        self.assertEqual(p.raise_shields(), 0)

    def test_generate_energy1(self):
        p = planet.Planet()
        p.on_surface.people = 1000
        p.player.race.pop_per_kt = 1000
        p.player.race.energy_per_10k_colonists = 1
        p.player.tech_level.propulsion = 10
        p.power_plants = 100
        self.assertEqual(p.generate_energy(), 151)

    def test_generate_energy2(self):
        p = planet.Planet()
        p.on_surface.people = 1000
        p.player.race.energy_per_10k_colonists = 0
        p.player.tech_level.propulsion = 4
        p.power_plants = 100
        self.assertEqual(p.generate_energy(), 120)

    def test_generate_energy3(self):
        p = planet.Planet()
        p.on_surface.people = 1000
        p.player.race.pop_per_kt = 1000
        p.player.race.energy_per_10k_colonists = 1000
        p.power_plants = 0
        self.assertEqual(p.generate_energy(), 1000)

    def test_mineral_availability1(self, mineral):
        p = planet.Planet()
        p.gravity = 50
        p.remaining_minerals = minerals.Minerals(titanium=10000, lithium=16000, silicon=24000)
        self.assertEqual(p.mineral_availability.titanium, .725)
        self.assertEqual(p.mineral_availability.lithium, 1.7)
        self.assertEqual(p.mineral_availability.silicon, 3.7)

    def test_mineral_availability2(self, mineral):
        p = planet.Planet()
        p.gravity = 10
        p.remaining_minerals = minerals.Minerals(titanium=3200, lithium=32000, silicon=8000)
        self.assertEqual(p.mineral_availability.titanium, .5)
        self.assertEqual(p.mineral_availability.lithium, 10) #max possible, remaining minerals is too high for size of world
        self.assertEqual(p.mineral_availability.silicon, 2.6)

    def test_mineral_availability3(self, mineral):
        p = planet.Planet()
        p.gravity = 100
        p.remaining_minerals = minerals.Minerals(titanium=49000, lithium=3500, silicon=70000)
        self.assertEqual(p.mineral_availability.titanium, 5)
        self.assertEqual(p.mineral_availability.lithium, 0.125)
        self.assertEqual(p.mineral_availability.silicon, 10) #max possible, remaining minerals too high


    def test_mine_minerals1(self):
        p = planet.Planet()
        p.on_surface.people = 100000
        #copy of test_mineral_availability1
        p.gravity = 50
        p.on_surface.titanium = 0
        p.on_surface.lithium = 0
        p.on_surface.silicon = 0
        p.remaining_minerals = minerals.Minerals(titanium=10000, lithium=16000, silicon=24000)
        self.assertEqual(p.mineral_availability.titanium, .725)
        self.assertEqual(p.mineral_availability.lithium, 1.7)
        self.assertEqual(p.mineral_availability.silicon, 3.7)
        p.mines = 1000
        p.player.tech_level.weapons = 0 #factor = 1.3
        p._mine_minerals()
        self.assertEqual(p.on_surface.titanium, 7.25)
        self.assertEqual(p.on_surface.lithium, 17)
        self.assertEqual(p.on_surface.silicon, 37)
        self.assertEqual(p.remaining_minerals.titanium, 9990.575)
        self.assertEqual(p.remaining_minerals.lithium, 15977.9)
        self.assertEqual(p.remaining_minerals.silicon, 23951.9)

    def test_mine_minerals2(self):
        p = planet.Planet()
        p.on_surface.people = 10000
        #copy of test_mineral_availability2
        p.gravity = 10
        p.on_surface.titanium = 0
        p.on_surface.lithium = 0
        p.on_surface.silicon = 0
        p.remaining_minerals = minerals.Minerals(titanium=3200, lithium=32000, silicon=8000)
        self.assertEqual(p.mineral_availability.titanium, .5)
        self.assertEqual(p.mineral_availability.lithium, 10) #max possible, remaining minerals is too high for size of world
        self.assertEqual(p.mineral_availability.silicon, 2.6)
        p.mines = 100
        p.player.tech_level.weapons = 14 #factor = 1.075
        p._mine_minerals()
        self.assertEqual(p.on_surface.titanium, .5)
        self.assertEqual(p.on_surface.lithium, 10)
        self.assertEqual(p.on_surface.silicon, 2.6)
        self.assertEqual(p.remaining_minerals.titanium, 3199.4625)
        self.assertEqual(p.remaining_minerals.lithium, 31989.25)
        self.assertEqual(p.remaining_minerals.silicon, 7997.205)


    def test_operate_factories(self):
        p = planet.Planet()
        p.on_surface.people = 1000
        p.player.tech_level.construction = 6
        p.factories = 25
        self.assertEqual(p.operate_factories(), 3)


    def test_auto_build(self):
        return #TODO
        p.on_surface.people = 1000
        p.mines = 25
        p.power_plants = 50
        p.factories = 2
        p.defenses = 4
        self.assertEqual(p.auto_build(), p.scanner_tech)
        p.mines = 25
        p.power_plants = 47
        p.factories = 25
        p.defenses = 4
        self.assertEqual(p.auto_build(), p.penetrating_tech)
        p.mines = 25
        p.power_plants = 3
        p.factories = 2
        p.defenses = 4
        #p.auto_build().debug_display()
        #p.facilities['Factory'].debug_display()
        self.assertEqual(p.auto_build() is p.facilities['Factory'], True, 'This error does not seem logical')#'FIX ME'
        p.mines = 2
        p.power_plants = 5
        p.factories = 2
        p.defenses = 1
        #p.auto_build().debug_display()
        #p.facilities['Defense'].debug_display()
        #self.assertEqual(p.auto_build(), p.facilities['Defense'], 'FIX ME')
        p.mines = 5
        p.power_plants = 3
        p.factories = 22
        p.defenses = 4
        #p.auto_build().debug_display()
        #p.facilities['Power'].debug_display()
        #self.assertEqual(p.auto_build(), p.facilities['Power'], 'FIX ME')
        p.mines = 2
        p.power_plants = 3
        p.factories = 26
        p.defenses = 4
        #p.auto_build().debug_display()
        #getattr(p, 'Mineral Extractor').debug_display()
        #self.assertEqual(p.auto_build(), getattr(p, 'Mineral Extractor'), 'FIX ME')
        ###reset###
        p = planet.Planet(name='Alpha Centauri', gravity=50, temperature=50, radiation=50)
        p.colonize(reference.Reference('Player', 'test_planet'), 'New Colony Minister')

