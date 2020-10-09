import sys
from .player import Player


""" Default values (default, min, max)  """
__defaults = {
    'research_current_energy_tech_level': [0, 0, 25],
    'research_current_weapons_tech_level': [0, 0, 25],
    'research_current_propulsion_tech_level': [0, 0, 25],
    'research_current_construction_tech_level': [0, 0, 25],
    'research_current_biotechnology_tech_level': [0, 0, 25],
    'research_bomb_1': [''],
    'research_bomb_1_cost': [0, 0, sys.maxsize]
    'research_bomb_2': [''],
    'research_bomb_2_cost': [0, 0, sys.maxsize]
    'research_bomb_3': [''],
    'research_bomb_3_cost': [0, 0, sys.maxsize]
    'research_bomb_4': [''],
    'research_bomb_4_cost': [0, 0, sys.maxsize]
    'research_bomb_5': [''],
    'research_bomb_5_cost': [0, 0, sys.maxsize]
    'research_bomb_6': [''],
    'research_bomb_6_cost': [0, 0, sys.maxsize]
    'research_bomb_7': [''],
    'research_bomb_7_cost': [0, 0, sys.maxsize]
    'research_bomb_8': [''],
    'research_bomb_8_cost': [0, 0, sys.maxsize]
    'research_cloak_1': [''],
    'research_cloak_1_cost': [0, 0, sys.maxsize]
    'research_cloak_2': [''],
    'research_cloak_2_cost': [0, 0, sys.maxsize]
    'research_cloak_3': [''],
    'research_cloak_3_cost': [0, 0, sys.maxsize]
    'research_cloak_4': [''],
    'research_cloak_4_cost': [0, 0, sys.maxsize]
    'research_ecm_1': [''],
    'research_ecm_1_cost': [0, 0, sys.maxsize]
    'research_ecm_2': [''],
    'research_ecm_2_cost': [0, 0, sys.maxsize]
    'research_ecm_3': [''],
    'research_ecm_3_cost': [0, 0, sys.maxsize]
    'research_ecm_4': [''],
    'research_ecm_4_cost': [0, 0, sys.maxsize]
    'research_defense_1': [''],
    'research_defense_1_cost': [0, 0, sys.maxsize]
    'research_defense_2': [''],
    'research_defense_2_cost': [0, 0, sys.maxsize]
    'research_defense_3': [''],
    'research_defense_3_cost': [0, 0, sys.maxsize]
    'research_defense_4': [''],
    'research_defense_4_cost': [0, 0, sys.maxsize]
    'research_defense_5': [''],
    'research_defense_5_cost': [0, 0, sys.maxsize]
    'research_defense_6': [''],
    'research_defense_6_cost': [0, 0, sys.maxsize]
    'research_defense_7': [''],
    'research_defense_7_cost': [0, 0, sys.maxsize]
    'research_defense_8': [''],
    'research_defense_8_cost': [0, 0, sys.maxsize]
    'research_depot_1': [''],
    'research_depot_1_cost': [0, 0, sys.maxsize]
    'research_depot_2': [''],
    'research_depot_2_cost': [0, 0, sys.maxsize]
    'research_depot_3': [''],
    'research_depot_3_cost': [0, 0, sys.maxsize]
    'research_depot_4': [''],
    'research_depot_4_cost': [0, 0, sys.maxsize]
    'research_depot_5': [''],
    'research_depot_5_cost': [0, 0, sys.maxsize]
    'research_depot_6': [''],
    'research_depot_6_cost': [0, 0, sys.maxsize]
    'research_depot_7': [''],
    'research_depot_7_cost': [0, 0, sys.maxsize]
    'research_depot_8': [''],
    'research_depot_8_cost': [0, 0, sys.maxsize]
    'research_engines_1': [''],
    'research_engines_1_cost': [0, 0, sys.maxsize]
    'research_engines_2': [''],
    'research_engines_2_cost': [0, 0, sys.maxsize]
    'research_engines_3': [''],
    'research_engines_3_cost': [0, 0, sys.maxsize]
    'research_engines_4': [''],
    'research_engines_4_cost': [0, 0, sys.maxsize]
    'research_engines_5': [''],
    'research_engines_5_cost': [0, 0, sys.maxsize]
    'research_engines_6': [''],
    'research_engines_6_cost': [0, 0, sys.maxsize]
    'research_engines_7': [''],
    'research_engines_7_cost': [0, 0, sys.maxsize]
    'research_engines_8': [''],
    'research_engines_8_cost': [0, 0, sys.maxsize]
    'research_hulls_1': [''],
    'research_hulls_1_cost': [0, 0, sys.maxsize]
    'research_hulls_2': [''],
    'research_hulls_2_cost': [0, 0, sys.maxsize]
    'research_hulls_3': [''],
    'research_hulls_3_cost': [0, 0, sys.maxsize]
    'research_hulls_4': [''],
    'research_hulls_4_cost': [0, 0, sys.maxsize]
    'research_hulls_5': [''],
    'research_hulls_5_cost': [0, 0, sys.maxsize]
    'research_hulls_6': [''],
    'research_hulls_6_cost': [0, 0, sys.maxsize]
    'research_hulls_7': [''],
    'research_hulls_7_cost': [0, 0, sys.maxsize]
    'research_hulls_8': [''],
    'research_hulls_8_cost': [0, 0, sys.maxsize]
    'research_mech_1': [''],
    'research_mech_1_cost': [0, 0, sys.maxsize]
    'research_mech_2': [''],
    'research_mech_2_cost': [0, 0, sys.maxsize]
    'research_mech_3': [''],
    'research_mech_3_cost': [0, 0, sys.maxsize]
    'research_mech_4': [''],
    'research_mech_4_cost': [0, 0, sys.maxsize]
    'research_mech_5': [''],
    'research_mech_5_cost': [0, 0, sys.maxsize]
    'research_mech_6': [''],
    'research_mech_6_cost': [0, 0, sys.maxsize]
    'research_mech_7': [''],
    'research_mech_7_cost': [0, 0, sys.maxsize]
    'research_mech_8': [''],
    'research_mech_8_cost': [0, 0, sys.maxsize]
    'research_orbital_1': [''],
    'research_orbital_1_cost': [0, 0, sys.maxsize]
    'research_orbital_2': [''],
    'research_orbital_2_cost': [0, 0, sys.maxsize]
    'research_orbital_3': [''],
    'research_orbital_3_cost': [0, 0, sys.maxsize]
    'research_orbital_4': [''],
    'research_orbital_4_cost': [0, 0, sys.maxsize]
    'research_orbital_5': [''],
    'research_orbital_5_cost': [0, 0, sys.maxsize]
    'research_orbital_6': [''],
    'research_orbital_6_cost': [0, 0, sys.maxsize]
    'research_orbital_7': [''],
    'research_orbital_7_cost': [0, 0, sys.maxsize]
    'research_orbital_8': [''],
    'research_orbital_8_cost': [0, 0, sys.maxsize]
    'research_planetary_1': [''],
    'research_planetary_1_cost': [0, 0, sys.maxsize]
    'research_planetary_2': [''],
    'research_planetary_2_cost': [0, 0, sys.maxsize]
    'research_planetary_3': [''],
    'research_planetary_3_cost': [0, 0, sys.maxsize]
    'research_planetary_4': [''],
    'research_planetary_4_cost': [0, 0, sys.maxsize]
    'research_planetary_5': [''],
    'research_planetary_5_cost': [0, 0, sys.maxsize]
    'research_planetary_6': [''],
    'research_planetary_6_cost': [0, 0, sys.maxsize]
    'research_planetary_7': [''],
    'research_planetary_7_cost': [0, 0, sys.maxsize]
    'research_planetary_8': [''],
    'research_planetary_8_cost': [0, 0, sys.maxsize]
    'research_scanner_1': [''],
    'research_scanner_1_cost': [0, 0, sys.maxsize]
    'research_scanner_2': [''],
    'research_scanner_2_cost': [0, 0, sys.maxsize]
    'research_scanner_3': [''],
    'research_scanner_3_cost': [0, 0, sys.maxsize]
    'research_scanner_4': [''],
    'research_scanner_4_cost': [0, 0, sys.maxsize]
    'research_scanner_5': [''],
    'research_scanner_5_cost': [0, 0, sys.maxsize]
    'research_scanner_6': [''],
    'research_scanner_6_cost': [0, 0, sys.maxsize]
    'research_scanner_7': [''],
    'research_scanner_7_cost': [0, 0, sys.maxsize]
    'research_scanner_8': [''],
    'research_scanner_8_cost': [0, 0, sys.maxsize]
    'research_weapons_1': [''],
    'research_weapons_1_cost': [0, 0, sys.maxsize]
    'research_weapons_2': [''],
    'research_weapons_2_cost': [0, 0, sys.maxsize]
    'research_weapons_3': [''],
    'research_weapons_3_cost': [0, 0, sys.maxsize]
    'research_weapons_4': [''],
    'research_weapons_4_cost': [0, 0, sys.maxsize]
    'research_weapons_5': [''],
    'research_weapons_5_cost': [0, 0, sys.maxsize]
    'research_weapons_6': [''],
    'research_weapons_6_cost': [0, 0, sys.maxsize]
    'research_weapons_7': [''],
    'research_weapons_7_cost': [0, 0, sys.maxsize]
    'research_weapons_8': [''],
    'research_weapons_8_cost': [0, 0, sys.maxsize]
    'research_queue_item_1': [''],
    'research_queue_item_2': [''],
    'research_queue_item_3': [''],
    'research_queue_item_4': [''],
    'research_queue_item_5': [''],
    'research_queue_item_6': [''],
    'research_queue_item_7': [''],
    'research_queue_item_8': [''],
}


""" """
class ResearchMinister(Player):
    """ Interact with UI """
    def _post(self, action, me):
        research_current_energy_tech_level = max(research_current_energy_tech_level, 0)  
        research_current_weapons_tech_level = max(research_current_weapons_tech_level, 0)
        research_current_propulsion_tech_level = max(research_current_propulsion_tech_level, 0)
        research_current_construction_tech_level = max(research_current_construction_tech_level, 0)
        research_current_biotechnology_tech_level = max(research_current_biotechnology_tech_level, 0)
        research_bomb_1 =  
        research_bomb_1_cost =
        research_bomb_2 =
        research_bomb_2_cost =
        research_bomb_3 =
        research_bomb_3_cost =
        research_bomb_4 =
        research_bomb_4_cost =
        research_bomb_5 =
        research_bomb_5_cost =
        research_bomb_6 =
        research_bomb_6_cost =
        research_bomb_7 =
        research_bomb_7_cost =
        research_bomb_8 =
        research_bomb_8_cost =
        research_cloak_1 = 
        research_cloak_1_cost = 
        research_cloak_2 = 
        research_cloak_2_cost = 
        research_cloak_3 = 
        research_cloak_3_cost = 
        research_cloak_4 = 
        research_cloak_4_cost = 
        research_ecm_1 = 
        research_ecm_1_cost = 
        research_ecm_2 = 
        research_ecm_2_cost = 
        research_ecm_3 = 
        research_ecm_3_cost = 
        research_ecm_4 = 
        research_ecm_4_cost = 
        research_defense_1 = 
        research_defense_1_cost = 
        research_defense_2 = 
        research_defense_2_cost = 
        research_defense_3  = 
        research_defense_3_cost = 
        research_defense_4 = 
        research_defense_4_cost = 
        research_defense_5 = 
        research_defense_5_cost = 
        research_defense_6 = 
        research_defense_6_cost = 
        research_defense_7 = 
        research_defense_7_cost = 
        research_defense_8 = 
        research_defense_8_cost = 
        research_depot_1 = 
        research_depot_1_cost = 
        research_depot_2 = 
        research_depot_2_cost = 
        research_depot_3 = 
        research_depot_3_cost = 
        research_depot_4 = 
        research_depot_4_cost = 
        research_depot_5 = 
        research_depot_5_cost = 
        research_depot_6 = 
        research_depot_6_cost = 
        research_depot_7 = 
        research_depot_7_cost = 
        research_depot_8 = 
        research_depot_8_cost = 
        research_engines_1 = 
        research_engines_1_cost = 
        research_engines_2 = 
        research_engines_2_cost = 
        research_engines_3 = 
        research_engines_3_cost = 
        research_engines_4 = 
        research_engines_4_cost = 
        research_engines_5 = 
        research_engines_5_cost = 
        research_engines_6 = 
        research_engines_6_cost = 
        research_engines_7 = 
        research_engines_7_cost = 
        research_engines_8 = 
        research_engines_8_cost = 
        research_hulls_1 = 
        research_hulls_1_cost = 
        research_hulls_2 = 
        research_hulls_2_cost = 
        research_hulls_3 = 
        research_hulls_3_cost = 
        research_hulls_4 = 
        research_hulls_4_cost = 
        research_hulls_5 = 
        research_hulls_5_cost = 
        research_hulls_6 = 
        research_hulls_6_cost = 
        research_hulls_7 = 
        research_hulls_7_cost = 
        research_hulls_8 = 
        research_hulls_8_cost = 
        research_mech_1 = 
        research_mech_1_cost = 
        research_mech_2 = 
        research_mech_2_cost = 
        research_mech_3 = 
        research_mech_3_cost = 
        research_mech_4 = 
        research_mech_4_cost = 
        research_mech_5 = 
        research_mech_5_cost = 
        research_mech_6 = 
        research_mech_6_cost = 
        research_mech_7 = 
        research_mech_7_cost = 
        research_mech_8 = 
        research_mech_8_cost = 
        research_orbital_1 = 
        research_orbital_1_cost = 
        research_orbital_2 = 
        research_orbital_2_cost = 
        research_orbital_3 = 
        research_orbital_3_cost = 
        research_orbital_4 = 
        research_orbital_4_cost = 
        research_orbital_5 = 
        research_orbital_5_cost = 
        research_orbital_6 = 
        research_orbital_6_cost = 
        research_orbital_7 = 
        research_orbital_7_cost = 
        research_orbital_8 = 
        research_orbital_8_cost = 
        research_planetary_1 = 
        research_planetary_1_cost = 
        research_planetary_2 = 
        research_planetary_2_cost = 
        research_planetary_3 = 
        research_planetary_3_cost = 
        research_planetary_4 = 
        research_planetary_4_cost = 
        research_planetary_5 = 
        research_planetary_5_cost = 
        research_planetary_6 = 
        research_planetary_6_cost = 
        research_planetary_7 = 
        research_planetary_7_cost = 
        research_planetary_8 = 
        research_planetary_8_cost = 
        research_scanner_1 = 
        research_scanner_1_cost = 
        research_scanner_2 = 
        research_scanner_2_cost = 
        research_scanner_3 = 
        research_scanner_3_cost = 
        research_scanner_4 = 
        research_scanner_4_cost = 
        research_scanner_5 = 
        research_scanner_5_cost = 
        research_scanner_6 = 
        research_scanner_6_cost = 
        research_scanner_7 = 
        research_scanner_7_cost = 
        research_scanner_8 = 
        research_scanner_8_cost = 
        research_weapons_1 = 
        research_weapons_1_cost = 
        research_weapons_2 = 
        research_weapons_2_cost = 
        research_weapons_3 = 
        research_weapons_3_cost = 
        research_weapons_4 = 
        research_weapons_4_cost = 
        research_weapons_5 = 
        research_weapons_5_cost = 
        research_weapons_6 = 
        research_weapons_6_cost = 
        research_weapons_7 = 
        research_weapons_7_cost = 
        research_weapons_8 = 
        research_weapons_8_cost = 
        research_queue_item_1 = 
        research_queue_item_2 = 
        research_queue_item_3 = 
        research_queue_item_4 = 
        research_queue_item_5 = 
        research_queue_item_6 = 
        research_queue_item_7 = 
    def calc_cost(self):
        energy_cost = research_modifier_energy * ((player.energy_tech_level ** 3) * 8 + 150)
        weapons_cost = research_modifier_weapons * ((player.weapons_tech_level ** 3) * 8 + 150) 
        propulsion_cost = research_modifier_propulsion * ((player.propulsion_tech_level ** 3) * 8 + 150)
        construction_cost = research_modifier_construction * ((player.construction_tech_level ** 3) * 8 + 150) 
        electronics_cost = research_modifier_electronics * ((player.electronics_tech_level ** 3) * 8 + 150)
        biotech_cost = research_modifier_biotechnology * ((player.biotechnology_tech_level ** 3) * 8 + 150)  

ResearchMinister.set_defaults(ResearchMinister, __defaults, no_reset=[])
