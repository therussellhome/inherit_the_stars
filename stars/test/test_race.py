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
        self.assertEqual(r.calc_points(), -197)
    def test_calc_points_research(self):
        r = race.Race(
                research_modifier_energy = 1000
        )
        self.assertEqual(r._calc_points_research(), -160)
        r = race.Race(
                research_modifier_weapons = 750
        )
        self.assertEqual(r._calc_points_research(), -140)
        r = race.Race(
                research_modifier_propulsion = 250
        )
        self.assertEqual(r._calc_points_research(), -160)
        r = race.Race(
                research_modifier_construction = 550
        )
        self.assertEqual(r._calc_points_research(), -156)
        r = race.Race(
                research_modifier_electronics = 950
        )
        self.assertEqual(r._calc_points_research(), -140)
        r = race.Race(
                research_modifier_biotechnology = 450
        )
        self.assertEqual(r._calc_points_research(), -144)
        
        r = race.Race(self.starting_tech_energy = 2)
        self.assertEqual(r._calc_points_research(), -166)
        
        r = race.Race(self.starting_tech_weapons = 4)
        self.assertEqual(r._calc_points_research(), -306)

        r = race.Race(self.starting_tech_propulsion = 1)
        self.assertEqual(r._calc_points_research(), -311)

        r = race.Race(self.starting_tech_construction = 3)
        self.assertEqual(r._calc_points_research(), -374)

        r = race.Race(self.starting_tech_electronics = 2)
        self.assertEqual(r._calc_points_research(), -396)

        r = race.Race(self.starting_tech_biotechnology = 1)
        self.assertEqual(r._calc_points_research(), -401)



    def test_calc_points_economy(self):
        r = race.Race(self.power_plants_per_10k_colonists = 2)
        self.assertEqual(r._calc_points_economy(), -700)

        r = race.Race(self.factories_per_10k_colonists = 50)
        self.assertEqual(r._calc_points_economy(), -1400)

        r = race.Race(self.mines_per_10k_colonists = 30)
        self.assertEqual(r._calc_points_economy(), -1800)
        
        r = race.Race(self.power_plants_per_10k_colonists = 20)
        self.assertEqual(r._calc_points_economy(), -2000)

        r = race.Race(self.energy_per_10k_colonists = 200)
        self.assertEqual(r._calc_points_economy(), -2060)

        r = race.Race(self.starting_colonists = 275000)
        self.assertEqual(r._calc_points_economy(), -2140)

        r = race.Race(self.cost_of_baryogenesis = 120000)
        self.assertEqual(r._calc_points_economy(), -2120)

        r = race.Race(self.starting mines = 20)
        self.assertEqual(r._calc_points_economy(), -2150)
        r = race.Race(self.starting_power_plants = 50)
        self.assertEqual(r._calc_points_economy(), -2200)
        r = race.Race(self.starting_factories = 0)
        self.assertEqual(r._calc_points_economy(), -2175)
        r = race.Race(self.starting_defenses = 0)
        self.assertEqual(r._calc_points_economy(), -2165)
        r = race.Race(self.starting_energy = 2000000)
        self.assertEqual(r._calc_points_economy(), -2265)
        r = race.Race(self.starting_lithium = 20)
        self.assertEqual(r._calc_points_economy(), -2265)


