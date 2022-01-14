import sys
from .defaults import Defaults
from math import log, exp

""" List of allowed primary race types """
PRIMARY_RACE_TRAITS = ['Aku\'Ultani', 'Kender', 'Formics', 'Gaerhule', 'Halleyforms', 'Melconians', 'Pa\'anuri', 'Patryns', 'TANSTAAFL']


""" Default values [default, min, max]  """
__defaults = {
    'ID': '@UUID',
    'icon_color': '#FFFFFF',
    'icon_class': 'fas fa-pastafarianism',
    'start_date': (3000, 0, sys.maxsize),
    'primary_race_trait': 'Melconians',
    'lrt_Trader': False,
    'lrt_Bioengineer': False,
    'lrt_SpacedOut': False,
    'lrt_Hypermiler': False,
    'lrt_McMansion': False,
    'lrt_MadScientist': False,
    'lrt_QuickHeal': False,
    'lrt_BleedingEdge': False,
    'lrt_Forager': True,
    'lrt_2ndSight': True,
    'lrt_JuryRigged': False,
    'research_modifier_energy': (500, 250, 1000),
    'research_modifier_weapons': (500, 250, 1000),
    'research_modifier_propulsion': (500, 250, 1000),
    'research_modifier_construction': (500, 250, 1000),
    'research_modifier_electronics': (500, 250, 1000),
    'research_modifier_biotechnology': (500, 250, 1000),
    'starting_tech_energy': (3, 0, 25),
    'starting_tech_weapons': (3, 0, 25),
    'starting_tech_propulsion': (3, 0, 25),
    'starting_tech_construction': (3, 0, 25),
    'starting_tech_electronics': (3, 0, 25),
    'starting_tech_biotechnology': (3, 0, 25),
    'hab_gravity': (14, 0, 100),
    'hab_gravity_stop': (86, 0, 100),
    'hab_gravity_immune': False,
    'hab_temperature': (14, 0, 100),
    'hab_temperature_stop': (86, 0, 100),
    'hab_temperature_immune': False,
    'hab_radiation': (14, 0, 100),
    'hab_radiation_stop': (86, 0, 100),
    'hab_radiation_immune': False,
    'growth_rate': (15, 5, 20),
    'body_mass': (80, 10, 160),
    'starting_colonists': (250000, 175000, 350000),
    'power_plants_per_10k_colonists': (10, 4, 25),
    'factories_per_10k_colonists': (10, 4, 25),
    'mineral_extractors_per_10k_colonists': (10, 4, 25),
    'defenses_per_10k_colonists': (10, 4, 25),
    'energy_per_10k_colonists': (1000, 100, 2000),
    'cost_of_baryogenesis': (1000, 200, 2000), # YJ / kT
    'scrap_rate': (50, 1, 100),
    'starting_factories': (10, 4, 25),
    'starting_mineral_extractors': (10, 4, 25),
    'starting_power_plants': (10, 4, 25),
    'starting_defenses': (10, 4, 25),
    'starting_energy': (165000, 50000, sys.maxsize),
    'starting_lithium': (500, 250, 1000),
    'starting_silicon': (500, 250, 1000),
    'starting_titanium': (500, 250, 1000),
    'message_file': '',
}

""" Advantage points gain/cost for each primary/lesser racial trait """
trait_cost = {
    'Aku\'Ultani': 6457, 
    'Kender': 6564, 
    'Formics': 6400, 
    'Gaerhule': 6510, 
    'Halleyforms': 6378, 
    'Pa\'anuri': 6420, 
    'Melconians': 6786, 
    'TANSTAAFL': 6509, 
    'Patryns': 6394,
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

econ_cost = {
    'Pa\'anuri_baryogenesis_invert_slope': 25/100.0,
    'Pa\'anuri_energy_cost_per_10k_col': .8,
    'cost_of_standard_research_mod': 133,
    'power_plant_cost_per_10k_col': 22.5,
    'factory_cost_per_10k_col': 17.5,
    'mineral_extractor_cost_per_10k_col': 11,
    'defense_cost_per_10k_col': 10,
    'energy_cost_per_10k_col': .6,
    'baryogenesis_invert_slope': 12/100.0,
    'scrap_rate_cost': 1.5,
}

start_cost = {
    'colonists': 4/5000,
    'factories': 5,
    'mineral_extractors': 3,
    'power_plants': 6,
    'defenses': 2,
#    'energy': 1/2500,
    'titanium': .2,
    'lithium': .2,
    'silicon': .2,
}


hab_cost = {
    'growthrate_cost': 128,
    'body_mass_cost': 6.4,
    'range_cost_per_click': 4,
    'grav_dis_slope': .8,
    'temp_dis_slope': 2,
    'rad_dis_slope': .8,
    'immunity_cost': 400,
    'immune_temp_extra_cost': 50,
}


""" Storage class for race parameters """
class Race(Defaults):
    """ Extract the color """
    def icon(self): # TODO test
        return '<i style="color: ' + self.icon_color + '; padding-right: 0" class="' + self.icon_class + '"></i>'

    """ Calculate the advantage points for this race (invalid race if <0) """
    def calc_points(self): # TODO test
        p = 0
        for t in self.list_traits():
            p += trait_cost[t]
        p += self._calc_points_research()
        p += self._calc_points_economy()
        p += self._calc_points_hab()
        p += self._calc_points_start()
        self._calc_starting_energy(p)
        return round(p)
    
    """ How many colonists per kT """
    def pop_per_kt(self):
        return 80000 / self.body_mass
    
    """ Make a list of the selected primary/lesser traits for this race """
    def list_traits(self):
        traits = [self.primary_race_trait]
        if self.lrt_Trader:
            traits.append('Trader')
        if self.lrt_Bioengineer:
            traits.append('Bioengineer')
        if self.lrt_SpacedOut:
            traits.append('SpacedOut')
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
    
    """ What percent of planets are habitable """
    def percent_planets_habitable(self): # TODO test
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
        overall_hab = 100.0 * max(overall_hab, 0.0001)
        return overall_hab
    
    """ Advantage points for habitability settings """
    def _calc_points_hab(self): # TODO test
        p = 0
        p -= self.growth_rate * hab_cost['growthrate_cost']
        # Cost of body mass
        p -= (160 - self.body_mass) * hab_cost['body_mass_cost']
        immunities = 0
        if self.hab_gravity_immune:
            immunities += 1
        else:
        # Cost of gravity range
            grav_range = self.hab_gravity_stop - self.hab_gravity
            grav_dis = abs((self.hab_gravity + self.hab_gravity_stop) / 2 - 50)
            p -= grav_range * hab_cost['range_cost_per_click'] - grav_dis * hab_cost['grav_dis_slope']
        if self.hab_temperature_immune:
            immunities += 1
            p -= hab_cost['immune_temp_extra_cost']
        else:
        # Cost of temperature range
            temp_range = self.hab_temperature_stop - self.hab_temperature
            temp_dis = abs((self.hab_temperature + self.hab_temperature_stop) / 2 - 50)
            p -= temp_range * hab_cost['range_cost_per_click'] - temp_dis * hab_cost['temp_dis_slope']
        if self.hab_radiation_immune:
            immunities += 1
        else:
        # Cost of radiation range
            rad_range = self.hab_radiation_stop - self.hab_radiation
            rad_dis = abs((self.hab_radiation + self.hab_radiation_stop) / 2 - 50)
            p -= rad_range * hab_cost['range_cost_per_click'] - rad_dis * hab_cost['rad_dis_slope']
        p -= (immunities ** 1.5) * hab_cost['immunity_cost'] * self.growth_rate/10
        return p
    
    """ Advantage points for economy settings """
    def _calc_points_economy(self):
        p = 0
        if self.primary_race_trait == 'Pa\'anuri': # TODO test
            p -= (1200 - self.cost_of_baryogenesis) * econ_cost['Pa\'anuri_baryogenesis_invert_slope']
            p -= econ_cost['Pa\'anuri_energy_cost_per_10k_col'] * self.energy_per_10k_colonists
        else:
            p -= econ_cost['power_plant_cost_per_10k_col'] * self.power_plants_per_10k_colonists
            p -= econ_cost['factory_cost_per_10k_col'] * self.factories_per_10k_colonists
            p -= econ_cost['mineral_extractor_cost_per_10k_col'] * self.mineral_extractors_per_10k_colonists
            p -= econ_cost['defense_cost_per_10k_col'] * self.defenses_per_10k_colonists
            p -= econ_cost['energy_cost_per_10k_col'] * self.energy_per_10k_colonists
            p -= (2000 - self.cost_of_baryogenesis) * econ_cost['baryogenesis_invert_slope']
        p -= self.scrap_rate * econ_cost['scrap_rate_cost']
        return p
    
    """ Advantage points for research settings """
    def _calc_points_research(self):
        p = 0
        tech_feilds = ['energy', 'weapons', 'propulsion', 'construction', 'electronics', 'biotechnology']
        for f in tech_feilds:
            if self['starting_tech_' + f] > 5:
                p -= 2 ** (self['starting_tech_' + f]/2 + 6)
            elif self['starting_tech_' + f] > 0:
                p -= 2 ** (self['starting_tech_' + f] + 3)
            p -= log(1000/self['research_modifier_' + f], 2)*econ_cost['cost_of_standard_research_mod']
        return round(p, 2)
    
    def _calc_points_start(self):
        p = 0
        if self.primary_race_trait == 'Pa\'anuri':
            for s in ['colonists', 'titanium', 'silicon', 'lithium']:
                p -= self['starting_' + s] * start_cost[s]
            return p
        for s in start_cost:
            p -= self['starting_' + s] * start_cost[s]
        return p
    
    def _calc_starting_energy(self, points):
        self.starting_energy = points * 2500 + 50000
    

Race.set_defaults(Race, __defaults, sparse_json=False)
