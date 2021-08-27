import unittest
from .. import stargate

class StargateTestCase(unittest.TestCase):
    def test_add1(self):
        s = stargate.Stargate()
        o = stargate.Stargate(strength=-2)
        self.assertEqual((s+o).strength, 0)
    def test_add2(self):
        s = stargate.Stargate(strength=500)
        o = stargate.Stargate(strength=-2)
        self.assertEqual((s+o).strength, 500)
    def test_add3(self):
        s = stargate.Stargate(strength=500)
        o = stargate.Stargate(strength=800)
        self.assertEqual((s+o).strength, 800)
    def test_add4(self):
        s = stargate.Stargate(strength=-500)
        o = stargate.Stargate(strength=-2)
        self.assertEqual((s+o).strength, 0)
    def test_add5(self):
        s = stargate.Stargate()
        o = stargate.Stargate()
        self.assertEqual((s+o).strength, 0)
    def test_add6(self):
        s = stargate.Stargate()
        o = stargate.Stargate(strength=2)
        self.assertEqual((s+o).strength, 2)

    def test_overgate1(self):
        s = stargate.Stargate(strength=500)
        self.assertEqual(round(s.overgate(300, 300, survival_test=True)), 107)
        self.assertLess(s.overgate(300, 300, 20), 133.8)
        self.assertGreater(s.overgate(300, 300, 20), 107)
    def test_overgate2(self):
        s = stargate.Stargate(strength=1000)
        self.assertEqual(round(s.overgate(600, 501, survival_test=True)), 64)
        self.assertLess(s.overgate(600, 501, 1), 384)
        self.assertGreater(s.overgate(600, 501, 1), 64)
    def test_overgate3(self):
        s = stargate.Stargate(strength=1000)
        self.assertEqual(round(s.overgate(620, 552, survival_test=True)), 128)
        self.assertLess(s.overgate(620, 552, 10), 192)
        self.assertGreater(s.overgate(620, 552, 10), 128)

