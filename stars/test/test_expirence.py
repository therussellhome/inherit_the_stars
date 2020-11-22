import unittest
from .. import *

class XPTest(unittest.TestCase):
    def test_calc(self):
        return #remove when done with fleet
        for i0 in range(32, 48):
            for i1 in range(32, 48):
                for i2 in range(32, 48):
                    for i3 in range(32, 64):
                        xp = expirence.Expirence(comishoning_date=i0, base_expirence=i1, battle_expirence=i2)
                        self.assertEqual(xp.calc(i3), sum([i0, i1, i2])-i3, msg=str([i0, i1, i2, i3]))


