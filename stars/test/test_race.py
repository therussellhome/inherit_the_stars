import unittest
from .. import *

class RaceTestCase(unittest.TestCase):
    def test_list_traits0(self):
        r = race.Race()
        self.assertEqual(r.list_traits(), ['Melconians'])
    
    def test_list_traits1(self):
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
                'Hypermiler',
                'McMansion',
                'MadScientist',
                'QuickHeal',
                'BleedingEdge',
                'Forager',
                '2ndSight',
                'JuryRigged'
        ])
    
    def test_list_traits2(self):
        r = race.Race(
            primary_race_trait = 'Pa\'anuri',
            lrt_MadScientist = True,
            lrt_QuickHeal = True,
            lrt_BleedingEdge = True,
            lrt_JuryRigged = True,
        )
        self.assertEqual(r.list_traits(), ['Pa\'anuri', 
                'MadScientist',
                'QuickHeal',
                'BleedingEdge',
                'JuryRigged'
        ])
    
    def test_list_traits3(self):
        r = race.Race(
            primary_race_trait = 'Halleyforms',
            lrt_Trader = True,
            lrt_Bioengineer = True,
            lrt_SpacedOut = True,
            lrt_WasteNot = True,
            lrt_Hypermiler = True,
            lrt_McMansion = True,
            lrt_Forager = True,
            lrt_2ndSight = True,
        )
        self.assertEqual(r.list_traits(), ['Halleyforms', 
                'Trader', 
                'Bioengineer', 
                'SpacedOut', 
                'Hypermiler',
                'McMansion',
                'Forager',
                '2ndSight',
        ])
    
    
    def test_calc_points_research00(self):
        r = race.Race(research_modifier_energy = 1000)
        self.assertEqual(r._calc_points_research(), -1250)
    
    def test_calc_points_research01(self):
        r = race.Race(research_modifier_weapons = 750)
        self.assertEqual(round(r._calc_points_research(), 2), -1353.76)
    
    def test_calc_points_research02(self):
        r = race.Race(research_modifier_propulsion = 250)
        self.assertEqual(round(r._calc_points_research(), 2), -1750)
    
    def test_calc_points_research03(self):
        r = race.Race(research_modifier_construction = 550)
        self.assertEqual(round(r._calc_points_research(), 3), -1465.624)
    
    def test_calc_points_research04(self):
        r = race.Race(research_modifier_electronics = 950)
        self.assertEqual(round(r._calc_points_research(), 2), -1268.5)
    
    def test_calc_points_research05(self):
        r = race.Race(research_modifier_biotechnology = 450)
        self.assertEqual(round(r._calc_points_research(), 2), -1538)
    
    def test_calc_points_research06(self):
        r = race.Race(starting_tech_energy = 2)
        self.assertEqual(r._calc_points_research(), -1532)
    
    def test_calc_points_research07(self):
        r = race.Race(starting_tech_weapons = 4)
        self.assertEqual(r._calc_points_research(), -1628)
    
    def test_calc_points_research08(self):
        r = race.Race(starting_tech_propulsion = 1)
        self.assertEqual(r._calc_points_research(), -1516)
    
    def test_calc_points_research09(self):
        r = race.Race(starting_tech_construction = 3)
        self.assertEqual(r._calc_points_research(), -1564)
    
    def test_calc_points_research10(self):
        r = race.Race(starting_tech_electronics = 11)
        self.assertEqual(round(r._calc_points_research(), 2), -4396.31)
    
    def test_calc_points_research11(self):
        r = race.Race(starting_tech_biotechnology = 8)
        self.assertEqual(r._calc_points_research(), -2524)
    
    
    def test_calc_points_economy00(self):
        r = race.Race(power_plants_per_10k_colonists = 2)
        self.assertEqual(r._calc_points_economy(), -925)
    
    def test_calc_points_economy01(self):
        r = race.Race(factories_per_10k_colonists = 50)
        self.assertEqual(r._calc_points_economy(), -1805)
    
    def test_calc_points_economy02(self):
        r = race.Race(mineral_extractors_per_10k_colonists = 30)
        self.assertEqual(r._calc_points_economy(), -1325)
        
    def test_calc_points_economy03(self):
        r = race.Race(power_plants_per_10k_colonists = 20)
        self.assertEqual(r._calc_points_economy(), -1330)
    
    def test_calc_points_economy04(self):
        r = race.Race(energy_per_10k_colonists = 200)
        self.assertEqual(r._calc_points_economy(), -925)
    
    def test_calc_points_economy05(self):
        r = race.Race(energy_per_10k_colonists = 2000)
        self.assertEqual(r._calc_points_economy(), -2005)
        
    def test_calc_points_economy07(self):
        r = race.Race(cost_of_baryogenesis = 1200)
        self.assertEqual(r._calc_points_economy(), -1081)
    
    
    def test_calc_points_start00(self):
        r = race.Race(starting_colonists = 275000)
        self.assertEqual(r._calc_points_start(), -830)
    
    def test_calc_points_start01(self):
        r = race.Race(starting_mineral_extractors = 20)
        self.assertEqual(r._calc_points_start(), -840)
    
    def test_calc_points_start02(self):
        r = race.Race(starting_power_plants = 20)
        self.assertEqual(r._calc_points_start(), -870)
    
    def test_calc_points_start03(self):
        r = race.Race(starting_factories = 5)
        self.assertEqual(r._calc_points_start(), -785)
    
    def test_calc_points_start04(self):
        r = race.Race(starting_defenses = 5)
        self.assertEqual(r._calc_points_start(), -800)
    
    def test_calc_points_start05(self):
        r = race.Race(starting_energy = 100000)
        self.assertEqual(r._calc_points_start(), -960)
        
    def test_calc_points_start06(self):
        r = race.Race(starting_lithium = 250)
        self.assertEqual(r._calc_points_start(), -760)
    

