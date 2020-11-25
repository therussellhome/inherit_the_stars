import unittest
from .. import *

class _TestPlayer:
    pass

class TechTestCase(unittest.TestCase):

    def test_is_available1(self):
        t = tech.Tech(level=tech_level.TechLevel(
            energy=1, 
            weapons=2, 
            propulsion=3, 
            construction=4, 
            electonics=5, 
            biotechnology=6
        ))
        l = tech_level.TechLevel()
        self.assertFalse(t.is_available(level=l))

    def test_is_available2(self):
        t = tech.Tech(level=tech_level.TechLevel(
            energy=1, 
            weapons=2, 
            propulsion=3, 
            construction=4, 
            electonics=5, 
            biotechnology=6
        ))
        l = tech_level.TechLevel(
            energy=6, 
            weapons=5, 
            propulsion=4, 
            construction=4, 
            electonics=5, 
            biotechnology=6
        )
        self.assertTrue(t.is_available(level=l))

    def test_is_available3(self):
        t = tech.Tech(race_requirements='Kender')
        r = race.Race()
        self.assertFalse(t.is_available(race=r))

    def test_is_available4(self):
        t = tech.Tech(race_requirements='Kender')
        r = race.Race(primary_race_trait='Kender')
        self.assertTrue(t.is_available(race=r))

    def test_is_available5(self):
        t = tech.Tech()
        r = race.Race()
        self.assertTrue(t.is_available(race=r))

    def test_is_available6(self):
        t = tech.Tech(race_requirements='Kender 2ndSight')
        r = race.Race(lrt_2ndSight=True)
        self.assertFalse(t.is_available(race=r))

    def test_is_available7(self):
        t = tech.Tech(race_requirements='Kender 2ndSight')
        r = race.Race(primary_race_trait='Kender', lrt_2ndSight=True)
        self.assertTrue(t.is_available(race=r))

    def test_is_available8(self):
        t = tech.Tech(race_requirements='-Akultan')
        r = race.Race()
        self.assertTrue(t.is_available(race=r))

    def test_is_available9(self):
        t = tech.Tech(race_requirements='Kender', level=tech_level.TechLevel(
            energy=1, 
            weapons=2, 
            propulsion=3, 
            construction=4, 
            electonics=5, 
            biotechnology=6
        ))
        l = tech_level.TechLevel(
            energy=6, 
            weapons=5, 
            propulsion=4, 
            construction=4, 
            electonics=5, 
            biotechnology=6
        )
        r = race.Race(primary_race_trait='Kender')
        self.assertTrue(t.is_available(level=l, race=r))
