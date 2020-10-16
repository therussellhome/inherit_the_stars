import sys
from .player import Player


""" Default values (default, min, max)  """
__defaults = {
    'research_current_energy_tech_level': [0, 0, 25],
    'research_current_weapons_tech_level': [0, 0, 25],
    'research_current_propulsion_tech_level': [0, 0, 25],
    'research_current_construction_tech_level': [0, 0, 25],
    'research_current_biotechnology_tech_level': [0, 0, 25],
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
        self.research_current_energy_tech_level = max(research_current_energy_tech_level, 0)  
        self.research_current_weapons_tech_level = max(research_current_weapons_tech_level, 0)
        self.research_current_propulsion_tech_level = max(research_current_propulsion_tech_level, 0)
        self.research_current_construction_tech_level = max(research_current_construction_tech_level, 0)
        self.research_current_biotechnology_tech_level = max(research_current_biotechnology_tech_level, 0)
        self.research_queue_item_1 = '' 
        self.research_queue_item_2 = ''
        self.research_queue_item_3 = ''
        self.research_queue_item_4 = ''
        self.research_queue_item_5 = ''
        self.research_queue_item_6 = ''
        self.research_queue_item_7 = ''
        self.research_queue_item_8 = ''
    def calc_cost(self):
        energy_cost = research_modifier_energy * ((player.energy_tech_level ** 3) * 8 + 150)
        weapons_cost = research_modifier_weapons * ((player.weapons_tech_level ** 3) * 8 + 150) 
        propulsion_cost = research_modifier_propulsion * ((player.propulsion_tech_level ** 3) * 8 + 150)
        construction_cost = research_modifier_construction * ((player.construction_tech_level ** 3) * 8 + 150) 
        electronics_cost = research_modifier_electronics * ((player.electronics_tech_level ** 3) * 8 + 150)
        biotech_cost = research_modifier_biotechnology * ((player.biotechnology_tech_level ** 3) * 8 + 150) 
    def research_bombs(self):
        pass
    def research_cloaks_and_ecm(self):
        pass
    def research_defense(self):
        pass
    def research_depot(self):
        pass
    def research_engines(self):
        pass
    def research_hulls(self):
        pass
    def research_mech(self):
        pass
    def research_orbital(self):
        pass
    def research_planetary(self):
        pass
    def research_scanners(self):
        pass
    def research_weapons(self):
        pass

ResearchMinister.set_defaults(ResearchMinister, __defaults, no_reset=[])
