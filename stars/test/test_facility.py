import unittest
from .. import *

class FacilityTestCase(unittest.TestCase):
    def test_cost1(self):
        f = facility.Facility(facility_type='power_plants')
        self.assertEqual(f.cost.energy, 250)

    def test_build1(self):
        f = facility.Facility(facility_type='power_plants')
        f.build()
        self.assertEqual(f.planet.power_plants, 0)

    def test_build2(self):
        f = facility.Facility(facility_type='power_plants')
        f.build(f.cost)
        self.assertEqual(f.planet.power_plants, 1)

    def test_build3(self):
        f = facility.Facility(facility_type='power_plants')
        f.planet.power_plants = 4
        f.build(f.cost)
        self.assertEqual(f.planet.power_plants, 5)

    def test_html1(self):
        f = facility.Facility(facility_type='power_plants')
        self.assertEqual(f.to_html(), 'Power Plant')
