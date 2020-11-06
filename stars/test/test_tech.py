import unittest
from .. import *

class _TestPlayer:
    pass

class TechTestCase(unittest.TestCase):
    def test_is_available(self):
        t = tech.Tech()
        t.level = tech_level.TechLevel(energy=1, weapons=2, propulsion=3, construction=4, electonics=5, biotechnology=6)
        p = _TestPlayer()
        p.race = race.Race()
        # test the tech level section
        p.tech_level = tech_level.TechLevel(energy=1)
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
        # test the race requirements section
        t.race_requirements = 'Kender'
        p.race.primary_race_trait = 'TANSTAAFL'
        self.assertFalse(t.is_available(p))
        t.race_requirements = 'Kender 2ndSight'
        p.race.lrt_2ndSight = True
        self.assertFalse(t.is_available(p))
        t.race_requirements = 'TANSTAAFL'
        self.assertTrue(t.is_available(p))
        t.race_requirements = 'Forager HyperMiler'
        p.race.lrt_Forager = True   
        self.assertFalse(t.is_available(p))
        t.race_requirements = '2ndSight'
        self.assertTrue(t.is_available(p))
        t.race_requirements = '-Akultan 2ndSight'
        self.assertTrue(t.is_available(p))
        t.race_requirements = '-Akultan 2ndSight Trader'
        self.assertFalse(t.is_available(p))
        t.race_requirements = '-TANSTAAFL 2ndSight Forager'
        self.assertFalse(t.is_available(p))