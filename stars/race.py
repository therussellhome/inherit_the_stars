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
    'energy_per_colonist': [5, 1, 20],
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
    'starting_lithium': [200, 200, 700], 
    'starting_silicon': [200, 200, 700], 
    'starting_titanium': [200, 200, 700], 
}

""" Advantage points gain/cost for each primary/lesser racial trait """
trait_cost = {
    'Aku\'Ultani': 667, 
    'Kender': 674, 
    'Formics': 470, 
    'Gaerhule': 520, 
    'Halleyforms': 588, 
    'Pa\'anuri': 670, 
    'Melconians': 496, 
    'TAANSTAFL': 719, 
    'Patryns': 604,
    'Trader': -126,
    'Bioengineer': -122,
    'SpacedOut': -81,
    'WasteNot': -76,
    'Hypermiler': -66,
    'McMansion': -55,
    'MadScientist': 10,
    'QuickHeal': 14,
    'BleedingEdge': 28,
    'Forager': -56,
    '2ndSight': -99,
    'JuryRigged': 109,
}

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
            if m > 100:
            p += (m / 100 - 1) ** 2 * 20 + (m / 100 - 1) * 30
        elif m < 100:
            p -= (m / 50 - 2) ** 2 * 20 - (m / 50 - 2) * 30
        return p

    """ Advantage points for economy settings """
    def _calc_points_economy(self):
        p = 0
        return p

    """ Advantage points for habitability settings """
    def _calc_points_habitability(self):
        p = 0
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
