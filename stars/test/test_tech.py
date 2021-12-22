import unittest
from .. import *

class _TestPlayer:
    pass

class TechTestCase(unittest.TestCase):

    def test_merge1(self):
        t1 = tech.Tech(category='a', armor=4, weapons=['w','e','a'])
        t2 = tech.Tech(category='b', armor=3, weapons=['p','o','n'])
        t1.merge(t2)
        self.assertEqual(t1.category, 'a')
        self.assertEqual(t1.armor, 7)
        self.assertEqual(t1.weapons, ['w','e','a','p','o','n'])

    def test_merge2(self):
        t1 = tech.Tech()
        t2 = tech.Tech()
        t1.hyperdenial.radius = 10
        t2.hyperdenial.radius = 20
        print(t2.hyperdenial)
        t1.merge(t2, max_not_merge=True)
        self.assertEqual(t1.hyperdenial.radius, 20)

    def test_merge3(self):
        t1 = tech.Tech()
        t2 = tech.Tech()
        t1.scanner.anti_cloak = 30
        t1.scanner.penetrating = 40
        t1.scanner.normal = 50
        t2.scanner.anti_cloak = 3
        t2.scanner.penetrating = 4
        t2.scanner.normal = 5
        t1.merge(t2, max_not_merge=True)
        self.assertEqual(t1.scanner.anti_cloak, 30)
        self.assertEqual(t1.scanner.penetrating, 40)
        self.assertEqual(t1.scanner.normal, 50)

    def test_group1(self):
        t = tech.Tech(category='Space Station Hull')
        self.assertEqual(t.tech_group(), 'Hulls & Mechanicals')

    def test_group2(self):
        t = tech.Tech(category='Bomb')
        self.assertEqual(t.tech_group(), 'Weapons')

    def test_group3(self):
        t = tech.Tech(category='Shield')
        self.assertEqual(t.tech_group(), 'Defense')

    def test_group4(self):
        t = tech.Tech(category='Scanner')
        self.assertEqual(t.tech_group(), 'Electronics')

    def test_group5(self):
        t = tech.Tech(category='Engine')
        self.assertEqual(t.tech_group(), 'Engines')

    def test_group6(self):
        t = tech.Tech(category='Orbital')
        self.assertEqual(t.tech_group(), 'Heavy Equipment')

    def test_group7(self):
        t = tech.Tech(category='category I made up myself')
        self.assertEqual(t.tech_group(), 'Other')

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
        r = race.Race(primary_race_trait='Akultan')
        self.assertFalse(t.is_available(race=r))

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

    def test_is_hull1(self):
        t = tech.Tech()
        self.assertFalse(t.is_hull())

    def test_is_hull2(self):
        t = tech.Tech(slots_depot=1)
        self.assertTrue(t.is_hull())

    def test_scrap1(self):
        t = tech.Tech(cost=cost.Cost(titanium=100))
        s = t.scrap_value(race.Race(scrap_rate=100))
        self.assertEqual(s.titanium, 100)

    def test_mini1(self):
        t = tech.Tech(level=tech_level.TechLevel(energy=10))
        self.assertEqual(t.miniaturization(), 1)

    def test_mini2(self):
        t = tech.Tech()
        self.assertEqual(t.miniaturization(tech_level.TechLevel(energy=9)), 1/1.3)

    def test_mini3(self):
        t = tech.Tech(level=tech_level.TechLevel(energy=10))
        self.assertEqual(t.miniaturization(tech_level.TechLevel(weapons=19)), 1)

    def test_mini4(self):
        t = tech.Tech(level=tech_level.TechLevel(energy=10))
        self.assertEqual(t.miniaturization(tech_level.TechLevel(energy=19)), 1/1.3)

    def test_buildcost1(self):
        t = tech.Tech(cost=cost.Cost(titanium=100))
        self.assertEqual(t.build_cost().titanium, 100)
