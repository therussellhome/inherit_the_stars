from .race import Race
from .defaults import Defaults
#a = COUNTIFS(E12:E25, Y1) #lesser race traits
#b = COUNTIFS(E28:E33, Y1)*2 #tech
#c = COUNTIFS(E40:E45, Y1)*2 #tech
#d = COUNTIFS(E52:E54, Y1)*10 #imunity
#left = 1000 - SUM(FILTER(C2:C80,E2:E80=Y1)) - (a+1)*(a/2) + (b+1)*(a/2)*10 - (c+1)*(c/2)*10 - (d+1)*(d/2)


__defaults = {
    "race_editor_primary_race_trait": ['Jack of all Trades'],
    "options_race_editor_primary_race_trait": [['Alternate Reality', 'Clam Adjuster', 'Hyper Expation', 'Inner Denial', 'Intersteler Travler', 'Jack of all Trades', 'Packit Phicics', 'Super Stelth', 'War Monger']],
    "race_editor_trader": [False],
    "race_editor_total_terraforming": [False],
    "race_editor_advanced_depot": [False],
    "race_editor_ultemet_recycling": [False],
    "race_editor_improved_fuel_efficiency": [False],
    "race_editor_improved_starbases": [False],
    "race_editor_generalized_research": [False],
    "race_editor_regenerating_shields": [False],
    "race_editor_bleeding_edge_technology": [False],
    "race_editor_no_antimatter_collecting_engines": [False],
    "race_editor_low_starting_popultion": [False],
    "race_editor_no_advanced_scanners": [False],
    "race_editor_cheap_engines": [False],
    "race_editor_energy_research_cost_modifier": [0, -1, 1],
    "race_editor_starting_tech_level_in_energy": [0, 0, 25],
    "race_editor_weapons_research_cost_modifier": [0, -1, 1],
    "race_editor_starting_tech_level_in_weapons": [0, 0, 25],
    "race_editor_propulsion_research_cost_modifier": [0, -1, 1],
    "race_editor_starting_tech_level_in_propulsion": [0, 0, 25],
    "race_editor_construction_research_cost_modifier": [0, -1, 1],
    "race_editor_starting_tech_level_in_construction": [0, 0, 25],
    "race_editor_electronics_research_cost_modifier": [0, -1, 1],
    "race_editor_starting_tech_level_in_electronics": [0, 0, 25],
    "race_editor_biotechnology_research_cost_modifier": [0, -1, 1],
    "race_editor_starting_tech_level_in_biotechnology": [0, 0, 25],
    "race_editor_effort_per_kt": [1000, 100, 9900],
    #"race_editor_display_effort_per_kt"
    "race_editor_energy_per_kt": [5, 1, 250]
}

class RaceEditor(Defaults):
    def post(self, action, **kwargs):
        self.__dict__.update(kwargs)


RaceEditor.set_defaults(RaceEditor, __defaults)
