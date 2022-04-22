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
