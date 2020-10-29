import unittest
from .. import *

class RaceTestCase(unittest.TestCase):
    def test_list_traits(self):
        r = race.Race(
            lrt_Trader = True,
            lrt_Bioengineer = True,
            lrt_SpacedOut = True,
            lrt_WasteNot = True,
            lrt_Hypermiler = True,
            lrt_McMansion = True,
            lrt_MadScientist = True,
            lrt_QuickHeal = True,
            lrt_BleedingEdge = True,
            lrt_Forager = True,
            lrt_2ndSight = True,
            lrt_JuryRigged = True,
        )
        self.assertEqual(r.list_traits(), ['Melconians', 
                'Trader', 
                'Bioengineer', 
                'SpacedOut', 
                'WasteNot',
                'Hypermiler',
                'McMansion',
                'MadScientist',
                'QuickHeal',
                'BleedingEdge',
                'Forager',
                '2ndSight',
                'JuryRigged'
        ])
