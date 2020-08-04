import unittest
from .. import *

class TechDisplayTestCase(unittest.TestCase):
    def setUp(self):
        self.tech = tech.Tech(name='test_tech_display')
        game_engine.register(self.tech)
        
    def test_post(self):
        display = tech_display.TechDisplay()
        display.post('test_tech_display')
        self.assertEqual(display.tech_name, 'test_tech_display')

        display.post('not_a_tech')
        self.assertEqual(display.tech_name, 'UNKNOWN')
