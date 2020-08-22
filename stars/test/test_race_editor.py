import unittest
from .. import *

class RaceEditorTestCase(unittest.TestCase):
    def setup(self):
        self.race = race_editor.RaceEditor()
    def test_calc_race_trait_cost(self):
        r = race_editor.RaceEditor(race_editor_primary_race_trait='Pa\'anuri')
        self.assertEqual(r.calc_race_trait_cost(), 0)
        r = race_editor.RaceEditor(race_editor_primary_race_trait='Halleyforms', race_editor_lrt_total_terraforming = True, race_editor_lrt_improved_fuel_efficiency = True)
        self.assertEqual(r.calc_race_trait_cost(), 462)
        r = race_editor.RaceEditor(race_editor_lrt_bleeding_edge_technology = True,
                                   race_editor_lrt_trader = True,
                                   race_editor_lrt_total_terraforming = True,
                                   race_editor_lrt_advanced_depot = True,
                                   race_editor_lrt_ultimate_recycling = True,
                                   race_editor_lrt_improved_fuel_efficiency = True,
                                   race_editor_lrt_improved_starbases = True,
                                   race_editor_lrt_generalized_research = True,
                                   race_editor_lrt_regenerating_shields = True,
                                   race_editor_lrt_no_antimatter_collecting_engines = True,
                                   race_editor_lrt_no_advanced_scanners = True,
                                   race_editor_lrt_cheap_engines = True)
        self.assertEqual(r.calc_race_trait_cost(), 542)
    def test_calc_reseach_cost(self):
        r = race_editor.RaceEditor(race_editor_starting_tech_biotechnology=25)
        self.assertEqual(r.calc_reseach_cost(), 31325)
        r = race_editor.RaceEditor(race_editor_starting_tech_biotechnology=3)
        self.assertEqual(r.calc_reseach_cost(), 63)
        r = race_editor.RaceEditor(race_editor_starting_tech_biotechnology=5)
        self.assertEqual(r.calc_reseach_cost(), 265)
        r = race_editor.RaceEditor(race_editor_starting_tech_biotechnology=10)
        self.assertEqual(r.calc_reseach_cost(), 2030)
        r = race_editor.RaceEditor(race_editor_research_modifier_energy=50, race_editor_research_modifier_weapons=50, race_editor_research_modifier_propulsion=50, race_editor_research_modifier_construction=50, race_editor_research_modifier_electronics=50, race_editor_research_modifier_biotechnology=50)
        self.assertEqual(r.calc_reseach_cost(), 900)
        r = race_editor.RaceEditor(race_editor_research_modifier_energy=200, race_editor_research_modifier_weapons=200, race_editor_research_modifier_propulsion=200, race_editor_research_modifier_construction=200, race_editor_research_modifier_electronics=200, race_editor_research_modifier_biotechnology=200)
        self.assertEqual(r.calc_reseach_cost(), -900)
        r = race_editor.RaceEditor(race_editor_research_modifier_energy=200, race_editor_research_modifier_weapons=50, race_editor_research_modifier_propulsion=200, race_editor_research_modifier_construction=50, race_editor_research_modifier_electronics=200, race_editor_research_modifier_biotechnology=50)
        self.assertEqual(r.calc_reseach_cost(), 0)
    def test_calc_hab_cost(self):
        r = race_editor.RaceEditor(race_editor_hab_temperature_immune = True, race_editor_hab_radiation_immune = True, race_editor_hab_gravity_immune = True)
        self.assertEqual(r.calc_hab_cost(), 2126)
        r = race_editor.RaceEditor(race_editor_hab_temperature = 0, race_editor_hab_temperature_stop = 0, race_editor_hab_radiation_immune = True, race_editor_hab_gravity_immune = True)
        self.assertEqual(r.calc_hab_cost(), 926)
        r = race_editor.RaceEditor(race_editor_hab_temperature = 0, race_editor_hab_temperature_stop = 0, race_editor_hab_radiation = 0, race_editor_hab_radiation_stop = 0, race_editor_hab_gravity = 0, race_editor_hab_gravity_stop = 0)
        self.assertEqual(r.calc_hab_cost(), -879)
        r = race_editor.RaceEditor(race_editor_hab_temperature = 0, race_editor_hab_temperature_stop = 100, race_editor_hab_radiation = 0, race_editor_hab_radiation_stop = 100, race_editor_hab_gravity = 0, race_editor_hab_gravity_stop = 100)
        self.assertEqual(r.calc_hab_cost(), 1021)
    def test_calc_economy_cost(self):
        r = race_editor.RaceEditor(race_editor_effort_per_colonist = 5, race_editor_energy_per_colonist = 0.2)
        self.assertEqual(r.calc_economy_cost(), 5500)
        r = race_editor.RaceEditor(race_editor_effort_per_colonist = 0.2, race_editor_energy_per_colonist = 0.01)
        self.assertEqual(r.calc_economy_cost(), -1961)
        r = race_editor.RaceEditor(race_editor_effort_per_colonist = 2)
        self.assertEqual(r.calc_economy_cost(), 1000)
        r = race_editor.RaceEditor(race_editor_energy_per_colonist = 0.1)
        self.assertEqual(r.calc_economy_cost(), 500)
        


