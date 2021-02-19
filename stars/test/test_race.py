import unittest
from .. import *

class RaceTestCase(unittest.TestCase):
    def test_list_traits(self):
        return #TODO
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
        self.assertEqual(r.calc_points(), -757)
    def test_calc_points_research(self):
        return #TODO
        r = race.Race(
                research_modifier_energy = 1000
        )
        self.assertEqual(r._calc_points_research(), -200)
        r = race.Race(
                research_modifier_weapons = 750
        )
        self.assertEqual(r._calc_points_research(), -220)
        r = race.Race(
                research_modifier_propulsion = 250
        )
        self.assertEqual(r._calc_points_research(), -260)
        r = race.Race(
                research_modifier_construction = 550
        )
        self.assertEqual(r._calc_points_research(), -236)
        r = race.Race(
                research_modifier_electronics = 950
        )
        self.assertEqual(r._calc_points_research(), -204)
        r = race.Race(
                research_modifier_biotechnology = 450
        )
        self.assertEqual(r._calc_points_research(), -244)
        
        r = race.Race(starting_tech_energy = 2)
        self.assertEqual(r._calc_points_research(), -262)
        
        r = race.Race(starting_tech_weapons = 4)
        self.assertEqual(r._calc_points_research(), -380)

        r = race.Race(starting_tech_propulsion = 1)
        self.assertEqual(r._calc_points_research(), -245)

        r = race.Race(starting_tech_construction = 3)
        self.assertEqual(r._calc_points_research(), -303)

        r = race.Race(starting_tech_electronics = 2)
        self.assertEqual(r.calc_points(), -259)

        r = race.Race(starting_tech_biotechnology = 1)
        self.assertEqual(r.calc_points(), -242)



    def test_calc_points_economy(self):
        return #TODO
        r = race.Race(power_plants_per_10k_colonists = 2)
        self.assertEqual(r._calc_points_economy(), -700)

        r = race.Race(factories_per_10k_colonists = 50)
        self.assertEqual(r._calc_points_economy(), -1580)

        r = race.Race(mines_per_10k_colonists = 30)
        self.assertEqual(r._calc_points_economy(), -1080)
        
        r = race.Race(power_plants_per_10k_colonists = 20)
        self.assertEqual(r._calc_points_economy(), -1105)

        r = race.Race(energy_per_10k_colonists = 200)
        self.assertEqual(r._calc_points_economy(), -940)
        r = race.Race(energy_per_10k_colonists = 200000)
        self.assertEqual(r._calc_points_economy(), -2020)
        
        r = race.Race(starting_colonists = 275000)
        self.assertEqual(r._calc_points_economy(), -900)

        r = race.Race(cost_of_baryogenesis = 120000)
        self.assertEqual(r._calc_points_economy(), -860)
        self.assertEqual(r.calc_points(), -217)

        r = race.Race(starting_mines = 20)
        self.assertEqual(r._calc_points_economy(), -910)
        self.assertEqual(r.calc_points(), -267)

        r = race.Race(starting_power_plants = 50)
        self.assertEqual(r._calc_points_economy(), -930)
        self.assertEqual(r.calc_points(), -287)

        r = race.Race(starting_factories = 0)
        self.assertEqual(r._calc_points_economy(), -855)

        r = race.Race(starting_defenses = 0)
        self.assertEqual(r._calc_points_economy(), -870)

        r = race.Race(starting_energy = 2000000)
        self.assertEqual(r._calc_points_economy(), -930)
        
        r = race.Race(starting_lithium = 20)
        self.assertEqual(r._calc_points_economy(), -880)


