import unittest
from ..tech import Tech
from ... import game_engine
from ...tech import Tech as TechItem
from ...engine import Engine
from ...tech_level import TechLevel
from ...weapon import Weapon

class TechDisplayTestCase(unittest.TestCase):
    def setUp(self):
        self.tech = TechItem(
            name = 'test_tech_display',
            level = TechLevel(energy=1, weapons=2, propulsion=3, construction=4, electronics=5, biotechnology=6),
            cargo_max = 9,
            fuel_max = 5,
            shield = 999,
            weapons = [Weapon()],
            engines = [Engine()],
            slots_orbital = 1
        )
        game_engine.register(self.tech)
        
    def test_post(self):
        display = Tech()
        display.post('test_tech_display')
        self.assertEqual(display.tech_name, 'test_tech_display')
        self.assertGreater(len(display.tech_level), 50)
        #TODO

        display.post('not_a_tech')
        self.assertEqual(display.tech_name, 'UNKNOWN')
