import unittest
from ..race_editor import RaceEditor

class RaceEditorTestCase(unittest.TestCase):
    def setup(self):
        self.race = RaceEditor()
    def test_calc_race_trait_cost(self):
        r = RaceEditor(race_editor_primary_race_trait='Pa\'anuri')
        self.assertEqual(r.calc_race_trait_cost(), 0)
        r = RaceEditor(race_editor_primary_race_trait='Halleyforms', race_editor_total_terraforming = True, race_editor_improved_fuel_efficiency = True)
#        self.assertEqual(r.calc_race_trait_cost(), 462)
        r = RaceEditor(race_editor_bleeding_edge_technology = True,
                                   race_editor_trader = True,
                                   race_editor_total_terraforming = True,
                                   race_editor_advanced_depot = True,
                                   race_editor_ultemet_recycling = True,
                                   race_editor_improved_fuel_efficiency = True,
                                   race_editor_improved_starbases = True,
                                   race_editor_generalized_research = True,
                                   race_editor_regenerating_shields = True,
                                   race_editor_no_antimatter_collecting_engines = True,
                                   race_editor_no_advanced_scanners = True,
                                   race_editor_cheap_engines = True)
#        self.assertEqual(r.calc_race_trait_cost(), 542)
    def test_calc_reseach_cost(self):
        r = RaceEditor(race_editor_starting_tech_level_in_biotechnology=25)
#        self.assertEqual(r.calc_reseach_cost(), 31325)
        r = RaceEditor(race_editor_starting_tech_level_in_biotechnology=3)
#        self.assertEqual(r.calc_reseach_cost(), 63)
        r = RaceEditor(race_editor_starting_tech_level_in_biotechnology=5)
#        self.assertEqual(r.calc_reseach_cost(), 265)
        r = RaceEditor(race_editor_starting_tech_level_in_biotechnology=10)
#        self.assertEqual(r.calc_reseach_cost(), 2030)
        r = RaceEditor(race_editor_energy_research_cost_modifier=50, race_editor_weapons_research_cost_modifier=50, race_editor_propulsion_research_cost_modifier=50, race_editor_construction_research_cost_modifier=50, race_editor_electronics_research_cost_modifier=50, race_editor_biotechnology_research_cost_modifier=50)
#        self.assertEqual(r.calc_reseach_cost(), 900)
        r = RaceEditor(race_editor_energy_research_cost_modifier=200, race_editor_weapons_research_cost_modifier=200, race_editor_propulsion_research_cost_modifier=200, race_editor_construction_research_cost_modifier=200, race_editor_electronics_research_cost_modifier=200, race_editor_biotechnology_research_cost_modifier=200)
#        self.assertEqual(r.calc_reseach_cost(), -900)
        r = RaceEditor(race_editor_energy_research_cost_modifier=200, race_editor_weapons_research_cost_modifier=50, race_editor_propulsion_research_cost_modifier=200, race_editor_construction_research_cost_modifier=50, race_editor_electronics_research_cost_modifier=200, race_editor_biotechnology_research_cost_modifier=50)
#        self.assertEqual(r.calc_reseach_cost(), 0)
    def test_calc_hab_cost(self):
        r = RaceEditor(race_editor_temperature_immune = True, race_editor_radiation_immune = True, race_editor_gravity_immune = True)
#        self.assertEqual(r.calc_hab_cost(), 2126)
        r = RaceEditor(race_editor_temperature = 0, race_editor_temperature_stop = 0, race_editor_radiation_immune = True, race_editor_gravity_immune = True)
#        self.assertEqual(r.calc_hab_cost(), 926)
        r = RaceEditor(race_editor_temperature = 0, race_editor_temperature_stop = 0, race_editor_radiation = 0, race_editor_radiation_stop = 0, race_editor_gravity = 0, race_editor_gravity_stop = 0)
#        self.assertEqual(r.calc_hab_cost(), -879)
        r = RaceEditor(race_editor_temperature = 0, race_editor_temperature_stop = 100, race_editor_radiation = 0, race_editor_radiation_stop = 100, race_editor_gravity = 0, race_editor_gravity_stop = 100)
#        self.assertEqual(r.calc_hab_cost(), 1021)
    def test_calc_economy_cost(self):
        r = RaceEditor(race_editor_effort_per_colonist = 5, race_editor_energy_per_colonist = 0.2)
        self.assertEqual(r.calc_economy_cost(), 5500)
        r = RaceEditor(race_editor_effort_per_colonist = 0.2, race_editor_energy_per_colonist = 0.01)
        self.assertEqual(r.calc_economy_cost(), -1961)
        r = RaceEditor(race_editor_effort_per_colonist = 2)
        self.assertEqual(r.calc_economy_cost(), 1000)
        r = RaceEditor(race_editor_energy_per_colonist = 0.1)
        self.assertEqual(r.calc_economy_cost(), 500)
        


