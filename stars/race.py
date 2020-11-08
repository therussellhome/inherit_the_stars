from .defaults import Defaults

""" Default values [default, min, max]  """
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
    'population_max': [10000000, 0, 1000000000],
    'starting_colonists': [250000, 175000, 350000],
    'colonists_to_operate_factory': [1000, 200, 5000],
    'colonists_to_operate_mine': [1000, 200, 5000],
    'colonists_to_operate_power_plant': [1000, 200, 5000],
    'colonists_to_operate_defense': [1000, 200, 5000],
    'energy_per_colonist': [5, 1, 20],
    'cost_of_baryogenesis': [10000, 2000, 12000],
    'starting_factories': [10, 5, 20],
    'starting_mines': [10, 5, 20],
    'starting_power_plants': [10, 5, 20],
    'starting_defenses': [10, 5, 20],
    'starting_energy': [50000, 25000, 100000],
    'starting_lithium': [200, 200, 700], 
    'starting_silicon': [200, 200, 700], 
    'starting_titanium': [200, 200, 700], 
}

""" Advantage points gain/cost for each primary/lesser racial trait """
trait_cost = {
    'Aku\'Ultani': 2467, 
    'Kender': 2474, 
    'Formics': 2270, 
    'Gaerhule': 2320, 
    'Halleyforms': 2388, 
    'Pa\'anuri': 2470, 
    'Melconians': 2296, 
    'TAANSTAFL': 2519, 
    'Patryns': 2404,
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


economy_costs = (
        'research_modifier_slope': 12.5,
        'growthrate_cost_per_click': 120,
        'factory_cost_per_click': 5, 
        'mine_slope': 100,
        'power_plant_slope': 100,
        'defense_slope': 100,
        'energy_slope': 100,
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


immunity_cost = {'grav_immunity_cost': 400, 'temp_immunity_cost': 450, 'rad_immunity_cost': 405}

""" Storage class for race parameters """
class Race(Defaults):
    """ Store values but do not load defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            p -= round( (1000 - m) / research_modifier_slope)
        return p

    """ Advantage points for economy settings """
    def _calc_points_economy(self):
        ap = 0
        ap -= (self.growth_rate - 5) * growthrate_cost_per_click
        ap -= (5000 - self.colonists_to_operate_factory) / (100 / factory_cost_per_click)
        ap -= round(20 - (1000 / self.colonists_to_operate_mine) * mine_slope)
        ap -= round(20 - (1000 / self.colonists_to_operate_power_plant) * power_plant_slope)
        ap -= round(20 - (1000 / self.colonists_to_operate_defense) * defense_slope)
        #print(ap)
        ap -= energy_slope * self.energy_per_colonist - energy_slope
        #print(ap)
        """Assuming starting_colonists increments are multiples of 5000, no need to round""" 
        ap -= population_slope * (self.starting_colonists - 175000) / 1000
        ap -= (12000 - self.cost_of_baryogenesis) / baryogenesis_invert_slope
        ap -= self.starting_factories * per_start_factory
        ap -= self.starting_mines * per_start_mine
        ap -= self.starting_power_plants * per_start_power_plant
        ap -= self.starting_defenses * per_start_defense
        ap -= self.starting_energy / 1000 * per_1000_start_energy
        ap -= self.starting_titanium / start_titanium_per_p
        ap -= self.starting_lithium / start_lithium_per_p
        ap -= self.starting_silicon / start_silicon_per_p
        return ap

    """ Advantage points for habitability settings """
    def _calc_points_habitability(self):
        p = 0
        # Cost of gravity range
            grav_range = self.hab_gravity_stop - self.hab_gravity + 1
            grav_dis = abs( (self.hab_gravity + self.hab_gravity_stop) / 2 - 50)
            p -= grav_range * 5 - 300 - grav_dis
        # Cost of temperature range
            temp_range = self.hab_temperature_stop - self.hab_temperature + 1
            temp_dis = abs( (self.hab_temperature + self.hab_temperatue_stop) / 2 - 50)
            p -= temp_range * 5 - 300 - temp_dis * 2
        # Cost of radiation range
            rad_range = self.hab_radiation_stop - self.hab_radiation + 1
            rad_dis = abs( (self.hab_radiation + self.hab_radiation_stop) / 2 - 50)
            p -= rad_range * 5 - 300 - rad_dis
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

Race.set_defaults(Race, __defaults)
