import sys
from math import log, exp
from .defaults import Defaults

""" Default values [default, min, max]  """
__defaults = {
    'name': [''],
    'icon': ['fas fa-pastafarianism'],
    'start_date': [3000, 0, sys.maxsize],
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
    'lrt_Forager': [False],
    'lrt_2ndSight': [False],
    'lrt_JuryRigged': [False],
    'research_modifier_energy': [500, 250, 1000],
    'research_modifier_weapons': [500, 250, 1000],
    'research_modifier_propulsion': [500, 250, 1000],
    'research_modifier_construction': [500, 250, 1000],
    'research_modifier_electronics': [500, 250, 1000],
    'research_modifier_biotechnology': [500, 250, 1000],
    'starting_tech_energy': [0, 0, 25],
    'starting_tech_weapons': [0, 0, 25],
    'starting_tech_propulsion': [0, 0, 25],
    'starting_tech_construction': [0, 0, 25],
    'starting_tech_electronics': [0, 0, 25],
    'starting_tech_biotechnology': [0, 0, 25],
    'hab_gravity': [0, 0, 100],
    'hab_gravity_stop': [100, 0, 100],
    'hab_gravity_immune': [False],
    'hab_temperature': [0, 0, 100],
    'hab_temperature_stop': [100, 0, 100],
    'hab_temperature_immune': [False],
    'hab_radiation': [0, 0, 100],
    'hab_radiation_stop': [100, 0, 100],
    'hab_radiation_immune': [False],
    'growth_rate': [15, 5, 20],
    'body_mass': [80, 10, 150],
    'starting_colonists': [250000, 175000, 350000],
    'power_plants_per_10k_colonists': [10, 2, 50],
    'factories_per_10k_colonists': [10, 2, 50],
    'mines_per_10k_colonists': [10, 2, 50],
    'defenses_per_10k_colonists': [10, 2, 50],
    'energy_per_10k_colonists': [100, 100, 2000],
    'cost_of_baryogenesis': [1000, 200, 1200], # YJ / kT
    'starting_factories': [10, 5, 20],
    'starting_mines': [10, 5, 20],
    'starting_power_plants': [10, 5, 20],
    'starting_defenses': [10, 5, 20],
    'starting_energy': [50000, 25000, 100000],
    'starting_lithium': [200, 200, 700], 
    'starting_silicon': [200, 200, 700], 
    'starting_titanium': [200, 200, 700], 
}


PRIMARY_RACE_TRAITS = ['Aku\'Ultani', 'Kender', 'Formics', 'Gaerhule', 'Halleyforms', 'Melconians', 'Pa\'anuri', 'Patryns', 'TANSTAAFL']


""" Advantage points gain/cost for each primary/lesser racial trait """
trait_cost = {
    'Aku\'Ultani': 2817, 
    'Kender': 2824, 
    'Formics': 2620, 
    'Gaerhule': 2670, 
    'Halleyforms': 2738, 
    'Pa\'anuri': 2820, 
    'Melconians': 3146, 
    'TAANSTAFL': 2869, 
    'Patryns': 2754,
    'Trader': -126,
    'Bioengineer': -122,
    '2ndSight': -99,
    'SpacedOut': -81,
    'WasteNot': -76,
    'Hypermiler': -66,
    'Forager': -56,
    'McMansion': -55,
    'MadScientist': 10,
    'QuickHeal': 14,
    'BleedingEdge': 28,
    'JuryRigged': 109,
}


economy_cost = {
    'research_modifier_slope': 12.5,
    'power_plant_cost_per_click': 45,
    'factory_cost_per_click': 35, 
    'mine_cost_per_click': 20,
    'defense_cost_per_click': 20,
    'energy_cost_per_click': 60,
    'population_slope': .8,
    'baryogenesis_invert_slope': 100,
    'per_start_factory': 5,
    'per_start_mine': 3,
    'per_start_power_plant': 5,
    'per_start_defense': 2,
    'per_1000_start_energy': 1,
    'start_titanium_per_p': 5,
    'start_lithium_per_p': 5,
    'start_silicon_per_p': 5,
}


habitability_cost = {
    'growthrate_cost_per_click': 120,
    'body_mass_cost_per_click': 64,
    'range_cost_per_click': 5,
    'immunity_fee': 50, #times number of immunities squared
    'grav_dis_slope': .5,
    'grav_immunity_cost': 400, 
    'temp_immunity_cost': 450, 
    'rad_immunity_cost': 405,
}

""" Storage class for race parameters """
class Race(Defaults):
    """ Store values but do not load defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.name == '':
            self.name = 'too lazy to name my race ' + str(id(self))

    """ Make a list of the selected primary/lesser traits for this race """
    def list_traits(self):
        traits = [self.primary_race_trait]
        if self.lrt_Trader:
            traits.append('Trader')
        if self.lrt_Bioengineer:
            traits.append('Bioengineer')
        if self.lrt_SpacedOut:
            traits.append('SpacedOut')
        if self.lrt_WasteNot:
            traits.append('WasteNot')
        if self.lrt_Hypermiler:
            traits.append('Hypermiler')
        if self.lrt_McMansion:
            traits.append('McMansion')
        if self.lrt_MadScientist:
            traits.append('MadScientist')
        if self.lrt_QuickHeal:
            traits.append('QuickHeal')
        if self.lrt_BleedingEdge:
            traits.append('BleedingEdge')
        if self.lrt_Forager:
            traits.append('Forager')
        if self.lrt_2ndSight:
            traits.append('2ndSight')
        if self.lrt_JuryRigged:
            traits.append('JuryRigged')
        return traits

    """ How many colonists per kT """
    def pop_per_kt(self):
        return 80000 / self.body_mass

    """ Scrap rate """
    def scrap_rate(self):
        if self.lrt_WasteNot:
            return 100
        return 50

    """ Calculate the advantage points for this race (invalid race if <0) """
    def calc_points(self):
        p = 0
        for t in self.list_traits():
            p += trait_cost[t]
        p += self._calc_points_research()
        p += self._calc_points_economy()
        p += self._calc_points_habitability()
        return p

    """ Advantage points for research settings """
    def _calc_points_research(self):
        p = 0
        # Purchased tech levels
        p -= self.starting_tech_energy ** 3 * 2 + self.starting_tech_energy * 3
        p -= self.starting_tech_weapons ** 3 * 2 + self.starting_tech_weapons * 3
        p -= self.starting_tech_propulsion ** 3 * 2 + self.starting_tech_propulsion * 3
        p -= self.starting_tech_construction ** 3 * 2 + self.starting_tech_construction * 3
        p -= self.starting_tech_electronics ** 3 * 2 + self.starting_tech_electronics * 3
        p -= self.starting_tech_biotechnology ** 3 * 2 + self.starting_tech_biotechnology * 3
        # Research modifiers
        researchmodifiers = [self.research_modifier_energy, 
            self.research_modifier_weapons, 
            self.research_modifier_propulsion,
            self.research_modifier_construction,
            self.research_modifier_electronics,
            self.research_modifier_biotechnology]
        for m in researchmodifiers: 
            p -= round((1000 - m) / economy_cost['research_modifier_slope'])
        return p

    """ Advantage points for economy settings """
    def _calc_points_economy(self):
        ap = 0
        ap -= economy_cost['power_plant_cost_per_click'] * (self.power_plants_per_10k_colonists - 2) / 2
        ap -= economy_cost['factory_cost_per_click'] * (self.factories_per_10k_colonists - 2) / 2
        ap -= economy_cost['mine_cost_per_click'] * (self.mines_per_10k_colonists - 2) / 2
        ap -= economy_cost['defense_cost_per_click'] * (self.defenses_per_10k_colonists - 2) / 2
        #print(ap)
        ap -= economy_cost['energy_cost_per_click'] * (self.energy_per_10k_colonists - 100) / 100
        #print(ap)
        ap -= round(economy_cost['population_slope'] * (self.starting_colonists - 175000) / 1000)
        ap -= (12000 - self.cost_of_baryogenesis) / economy_cost['baryogenesis_invert_slope']
        ap -= self.starting_factories * economy_cost['per_start_factory']
        ap -= self.starting_mines * economy_cost['per_start_mine']
        ap -= self.starting_power_plants * economy_cost['per_start_power_plant']
        ap -= self.starting_defenses * economy_cost['per_start_defense']
        ap -= self.starting_energy / 1000 * economy_cost['per_1000_start_energy']
        ap -= self.starting_titanium / economy_cost['start_titanium_per_p']
        ap -= self.starting_lithium / economy_cost['start_lithium_per_p']
        ap -= self.starting_silicon / economy_cost['start_silicon_per_p']
        return ap

    """ Advantage points for habitability settings """
    def _calc_points_habitability(self):
        p = 0
        p -= (self.growth_rate - 5) * habitability_cost['growthrate_cost_per_click']
        # Cost of body mass
        p -= (150 - self.body_mass) * habitability_cost['body_mass_cost_per_click'] / 10

        immunities = 0
        if self.hab_gravity_immune:
            immunities += 1
            p -= habitability_cost['grav_immunity_cost']
        else:
        # Cost of gravity range
            grav_range = self.hab_gravity_stop - self.hab_gravity + 1
            grav_dis = abs((self.hab_gravity + self.hab_gravity_stop) / 2 - 50)
            p -= grav_range * habitability_cost['range_cost_per_click'] - 300 - grav_dis * habitability_cost['grav_dis_slope']
        if self.hab_temperature_immune:
            immunities += 1
            p -= habitability_cost['temp_immunity_cost']
        else:
        # Cost of temperature range
            temp_range = self.hab_temperature_stop - self.hab_temperature + 1
            temp_dis = abs((self.hab_temperature + self.hab_temperature_stop) / 2 - 50)
            p -= temp_range * habitability_cost['range_cost_per_click'] - 300 - temp_dis * 2
        if self.hab_radiation_immune:
            immunities += 1
            p -= habitability_cost['rad_immunity_cost']
        else:
        # Cost of radiation range
            rad_range = self.hab_radiation_stop - self.hab_radiation + 1
            rad_dis = abs((self.hab_radiation + self.hab_radiation_stop) / 2 - 50)
            p -= rad_range * habitability_cost['range_cost_per_click'] - 300 - rad_dis

        p -= (immunities ** 2) * habitability_cost['immunity_fee'] + immunities * 5
        return p

    """ What percent of planets are habitable """
    def percent_planets_habitable(self):
        overall_hab = 1.0
        if not self.hab_gravity_immune:
            hab = 0.0
            for i in range(self.hab_gravity, self.hab_gravity_stop + 1):
                hab += (100.0 - i) * 2.0 / 101.0
            overall_hab *= hab / 100.0
        if not self.hab_temperature_immune:
            hab = 0.0
            for i in range(self.hab_temperature, self.hab_temperature_stop + 1):
                hab += 1.7 * exp(-1.0 * (((i - 50.0) * (i - 50.0)) / (2.0 * 27.0 * 27.0))) - 0.1
            overall_hab *= hab / 100.0
        if not self.hab_radiation_immune:
            hab = 0.0
            for i in range(self.hab_radiation, self.hab_radiation_stop + 1):
                hab += 100.0/101.0
            overall_hab *= hab / 100.0
        overall_hab = 100.0 * max(overall_hab, 0.001)
        return overall_hab

Race.set_defaults(Race, __defaults, sparse_json=False)
