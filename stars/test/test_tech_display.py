import unittest
from .. import *

class TechDisplayTestCase(unittest.TestCase):
    def setUp(self):
        self.tech = tech.Tech(
            name = 'test_tech_display',
            level = tech_level.TechLevel(energy=1, weapons=2, propulsion=3, construction=4, electronics=5, biotechnology=6),
            cargo_max = 9,
            fuel_max = 5,
            shield = 999,
            weapons = [weapon.Weapon()],
            engines = [engine.Engine()],
            slots_orbital = 1
        )
        game_engine.register(self.tech)
        
    def test_post(self):
        display = tech_display.TechDisplay()
        display.post('test_tech_display')
        self.assertEqual(display.tech_name, 'test_tech_display')
        self.assertGreater(len(display.tech_level), 50)
        #TODO

        display.post('not_a_tech')
        self.assertEqual(display.tech_name, 'UNKNOWN')
