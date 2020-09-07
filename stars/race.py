from .defaults import Defaults

""" Default values (default, min, max)  """
__defaults = {
    'name': [''],
    'primary_race_trait': ['Melconians'],
    'lrt_Trader': [False],
    'lrt_Bioengineer': [False],
    'lrt_SpacedOut': [False],
    'lrt_WasteNot': [False],
    'lrt_Hypermiler': [False],
    'lrt_McMansion': [False],
    'lrt_MadScientist': [False],
    'lrt_QuickHeal': [False],
    'lrt_BleedingEdge': [False],
    'lrt_Forager': [True],
    'lrt_2ndSight': [True],
    'lrt_JuryRigged': [False],
    'research_modifier_energy': [100, 50, 200],
    'research_modifier_weapons': [100, 50, 200],
    'research_modifier_propulsion': [100, 50, 200],
    'research_modifier_construction': [100, 50, 200],
    'research_modifier_electronics': [100, 50, 200],
    'research_modifier_biotechnology': [100, 50, 200],
    'starting_tech_energy': [0, 0, 25],
    'starting_tech_weapons': [0, 0, 25],
    'starting_tech_propulsion': [0, 0, 25],
    'starting_tech_construction': [0, 0, 25],
    'starting_tech_electronics': [0, 0, 25],
    'starting_tech_biotechnology': [0, 0, 25],
    'effort_per_colonist': [1.0, 0.2, 5.0],
    'energy_per_colonist': [5, 1, 20],
    'minerals_per_mine': [3, 1, 9],
    'hab_gravity': [0, 0, 100],
    'hab_gravity_stop': [100, 0, 100],
    'hab_gravity_immune': [False],
    'hab_temperature': [0, 0, 100],
    'hab_temperature_stop': [100, 0, 100],
    'hab_temperature_immune': [False],
    'hab_radiation': [0, 0, 100],
    'hab_radiation_stop': [100, 0, 100],
    'hab_radiation_immune': [False],
    'growth_rate': [15, 1, 20],
    'starting_colonists': [250, 175, 350],
    'population_max': [10000000, 0, 1000000000],
    'starting_factories': [10, 5, 20],
    'starting_mines': [10, 5, 20],
    'starting_power_plants': [10, 5, 20],
    'starting_defenses': [10, 5, 20],
    'cost_of_baryogenesis': [10000, 2000, 12000],
    'colonists_to_operate_factory': [1000, 200, 5000],
    'colonists_to_operate_mine': [1000, 200, 5000],
    'colonists_to_operate_power_plant': [1000, 200, 5000],
    'colonists_to_operate_defense': [1000, 200, 5000],
    'starting_energy': [50000, 25000, 100000],
    'starting_lithium': [500, 400, 700], 
    'starting_silicon': [500, 400, 700], 
    'starting_titanium': [500, 400, 700], 
}

""" Storage class for race parameters """
class Race(Defaults):
    """ Store values but do not load defaults """
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]


Race.set_defaults(Race, __defaults)
