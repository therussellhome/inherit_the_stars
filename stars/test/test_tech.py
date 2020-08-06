import unittest
from .. import *

class _TestPlayer:
    pass

class TechTestCase(unittest.TestCase):
    def test_is_available(self):
        t = tech.Tech()
        t.level = tech_level.TechLevel(evergy=1, weapons=2, propulsion=3, construction=4, electonics=5, biotechnology=6)
        p = _TestPlayer()
        p.tech_level = tech_level.TechLevel(evergy=1)
        self.assertFalse(t.is_available(p))
        p.tech_level.weapons = 2
        self.assertFalse(t.is_available(p))
        p.tech_level.propulsion = 3
        self.assertFalse(t.is_available(p))
        p.tech_level.construction = 4
        self.assertFalse(t.is_available(p))
        p.tech_level.electronics = 5
        self.assertFalse(t.is_available(p))
        p.tech_level.biotechnology = 6
        self.assertTrue(t.is_available(p))
        p.tech_level.energy = 2
        self.assertTrue(t.is_available(p))
