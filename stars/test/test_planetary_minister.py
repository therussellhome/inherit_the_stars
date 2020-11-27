import unittest
from .. import *

class PlanetaryMinisterTestCase(unittest.TestCase):
    def test_equalization(self):
        m = planetary_minister.PlanetaryMinister()
        setattr(m, 'Power Plant', 30)
        setattr(m, 'Factory', 50)
        setattr(m, 'Mineral Extractor',  260)
        setattr(m, 'Planetary Shield', 60)
        m.normalize()
        self.assertEqual(getattr(m, 'Power Plant'), 14)
        self.assertEqual(getattr(m, 'Factory'), 20)
        self.assertEqual(getattr(m, 'Mineral Extractor'), 41)
        self.assertEqual(getattr(m, 'Planetary Shield'), 25)
