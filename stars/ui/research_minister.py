from .playerui import PlayerUI


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
class ResearchMinister(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)


ResearchMinister.set_defaults(ResearchMinister, __defaults)
