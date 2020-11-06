import sys
from .player import Player


""" Default values (default, min, max)  """
__defaults = {
    'research_current_energy_tech_level': [0, 0, sys.maxsize],
    'research_current_weapons_tech_level': [0, 0, sys.maxsize],
    'research_current_propulsion_tech_level': [0, 0, sys.maxsize],
    'research_current_construction_tech_level': [0, 0, sys.maxsize],
    'research_current_biotechnology_tech_level': [0, 0, sys.maxsize],
    'research_weapons': [[]],
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
        self.research_current_energy_tech_level = max(min(research_current_energy_tech_level, 25), 0)  
        self.research_current_weapons_tech_level = max(min(research_current_weapons_tech_level, 25), 0)
        self.research_current_propulsion_tech_level = max(min(research_current_propulsion_tech_level, 25), 0)
        self.research_current_construction_tech_level = max(min(research_current_construction_tech_level, 25), 0)
        self.research_current_electronics_tech_level = max(min(research_current_electronics_tech_level, 25), 0)
        self.research_current_biotechnology_tech_level = max(min(research_current_biotechnology_tech_level, 25), 0)
        self.research_weapons = ['<td>weapon 1</td>', '<td>weapon 2</td>']
        self.research_queue_item_1 = me.research_queue[0] 
        self.research_queue_item_2 = me.research_queue[1] 
        self.research_queue_item_3 = me.research_queue[2] 
        self.research_queue_item_4 = me.research_queue[3] 
        self.research_queue_item_5 = me.research_queue[4] 
        self.research_queue_item_6 = me.research_queue[5] 
        self.research_queue_item_7 = me.research_queue[6] 
        self.research_queue_item_8 = me.research_queue[7] 
    def calc_cost(self, field):
        if field == 'energy':
            return round(research_modifier_energy * ((player.energy_tech_level ** 3) * 8 + 150))
        if field == 'weapons':
            return round(research_modifier_weapons * ((player.weapons_tech_level ** 3) * 8 + 150)) 
        if field == 'propulsion':
            return round(research_modifier_propulsion * ((player.propulsion_tech_level ** 3) * 8 + 150))
        if field == 'construction':
            return round(research_modifier_construction * ((player.construction_tech_level ** 3) * 8 + 150)) 
        if field == 'electronics':
            return round(research_modifier_electronics * ((player.electronics_tech_level ** 3) * 8 + 150))
        if field == 'biotechnology':
            return round(research_modifier_biotechnology * ((player.biotechnology_tech_level ** 3) * 8 + 150))
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
