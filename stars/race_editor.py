from math import log
from .race import Race
from .defaults import Defaults
#s = SUM(FILTER(C2:C80,E2:E80=Y1)) #total
#b = COUNTIFS(E28:E33, Y1)*2 #tech
#c = COUNTIFS(E40:E45, Y1)*2 #tech
#left = -s + (b+1)*(b/2)*10 - (c+1)*(c/2)*10


__defaults = {
    'race_editor_primary_race_trait': ['Jack of all Trades'],
    'options_race_editor_primary_race_trait': [['Aku\'Ultani', 'Cushgars', 'Formics', 'Gaerhules', 'Halleyforms', 'Melconians', 'Pa\'anuri', 'Patryns', 'TANSTAAFL']],
    'race_editor_trader': [False],
    'race_editor_total_terraforming': [False],
    'race_editor_advanced_depot': [False],
    'race_editor_ultemet_recycling': [False],
    'race_editor_improved_fuel_efficiency': [False],
    'race_editor_improved_starbases': [False],
    'race_editor_generalized_research': [False],
    'race_editor_regenerating_shields': [False],
    'race_editor_bleeding_edge_technology': [False],
    'race_editor_no_antimatter_collecting_engines': [False],
    'race_editor_low_starting_popultion': [False],
    'race_editor_no_advanced_scanners': [False],
    'race_editor_cheap_engines': [False],
    'race_editor_energy_research_cost_modifier': [100, 50, 200],
    'race_editor_starting_tech_level_in_energy': [0, 0, 25],
    'race_editor_weapons_research_cost_modifier': [100, 50, 200],
    'race_editor_starting_tech_level_in_weapons': [0, 0, 25],
    'race_editor_propulsion_research_cost_modifier': [100, 50, 200],
    'race_editor_starting_tech_level_in_propulsion': [0, 0, 25],
    'race_editor_construction_research_cost_modifier': [100, 50, 200],
    'race_editor_starting_tech_level_in_construction': [0, 0, 25],
    'race_editor_electronics_research_cost_modifier': [100, 50, 200],
    'race_editor_starting_tech_level_in_electronics': [0, 0, 25],
    'race_editor_biotechnology_research_cost_modifier': [100, 50, 200],
    'race_editor_starting_tech_level_in_biotechnology': [0, 0, 25],
    'race_editor_effort_per_colonist': [1.0, 0.2, 5.0],
    #'race_editor_display_effort_per_colonist'
    'race_editor_energy_per_colonist': [0.05, 0.01, 0.1],
    'race_editor_gravity': [0, 0, 100],
    'race_editor_gravity_stop': [100, 0, 100],
    'race_editor_gravity_immune': [False],
    'race_editor_temperature': [0, 0, 100],
    'race_editor_temperature_stop': [100, 0, 100],
    'race_editor_temperature_immune': [False],
    'race_editor_radiation': [0, 0, 100],
    'race_editor_radiation_stop': [100, 0, 100],
    'race_editor_radiation_immune': [False],
}
def calc_hab_cost(start, stop): #not temperature
    size = stop - start + 1
    dis = abs((start+stop)/2 - 50)
    return (size*5 - 300) - dis*2


class RaceEditor(Defaults):
    """ finish this """
    """ calulate the cost of race traits """
    def calc_race_trait_cost(self):
        aps = 0
        lrts = 0
        if self.race_editor_primary_race_trait == 'Alternate Reality':
            pass
        elif self.race_editor_primary_race_trait == 'Clam Adjuster':
            aps += 268
        elif self.race_editor_primary_race_trait == 'Hyper Expation':
            pass
        elif self.race_editor_primary_race_trait == 'Inner Denial':
            pass
        elif self.race_editor_primary_race_trait == 'Intersteler Travler':
            aps += 284
        elif self.race_editor_primary_race_trait == 'Jack of all Trades':
            aps += 176
        elif self.race_editor_primary_race_trait == 'Packit Phicics':
            aps += 399
        elif self.race_editor_primary_race_trait == 'Super Stelth':
            aps += 354
        elif self.race_editor_primary_race_trait == 'War Monger':
            aps += 347
        if self.race_editor_trader:
            aps += 126
            lrts += 1
        if self.race_editor_total_terraforming:
            aps += 122
            lrts += 1
        if self.race_editor_advanced_depot:
            aps += 81
            lrts += 1
        if self.race_editor_ultemet_recycling:
            aps += 76
            lrts += 1
        if self.race_editor_improved_fuel_efficiency:
            aps += 66
            lrts += 1
        if self.race_editor_improved_starbases:
            aps += 55
            lrts += 1
        if self.race_editor_generalized_research:
            aps += -10
            lrts += 1
        if self.race_editor_regenerating_shields:
            aps += -14
            lrts += 1
        if self.race_editor_bleeding_edge_technology:
            aps += -28
            lrts += 1
        if self.race_editor_no_antimatter_collecting_engines:
            aps += -56
            lrts += 1
        #if self.race_editor_low_starting_popultion:
        #    aps += -62
        #    lrts += 1
        if self.race_editor_no_advanced_scanners:
            aps += -99
            lrts += 1
        if self.race_editor_cheap_engines:
            aps += -109
            lrts += 1
        aps += (lrts+1) * lrts
        return aps
    def post(self, action):
        """ aply the cost of race traits """
        ap = 1000 - self.calc_race_trait_cost()
        """ calculate and aply the cost of habitablilaty """
        immunitys = 0
        if self.race_editor_gravity_immune:
            self.race_editor_gravity = 0
            self.race_editor_gravity_stop = 100
            immunitys += 1
            ap -= 400
        else:
            ap -= calc_hab_cost(self.race_editor_gravity, self.race_editor_gravity_stop)
        if self.race_editor_temperature_immune:
            self.race_editor_temperature = 0
            self.race_editor_temperature_stop = 100
            immunitys += 1
            ap -= 450
        else:
            size = self.race_editor_temperature_stop - self.race_editor_temperature + 1
            dis = abs((self.race_editor_temperature + self.race_editor_temperature_stop)/2 - 50)
            ap -= (size*5 - 300) - dis*4
        if self.race_editor_radiation_immune:
            self.race_editor_radiation = 0
            self.race_editor_radiation_stop = 100
            immunitys += 1
            ap -= 405
        else:
            ap -= calc_hab_cost(self.race_editor_radiation, self.race_editor_radiation_stop)
        ap -= (immunitys*10)+1 * (immunitys*5)
        """ calulate and aply the cost of the econimy """
        c = ((self.race_editor_effort_per_colonist)-1)*1000 + ((((self.race_editor_effort_per_colonist)-1)*10)+1) * self.race_editor_effort_per_colonist*10
        if self.race_editor_effort_per_colonist > 1:
            c /= 2
        ap -= c
        c = round(log(self.race_editor_energy_per_colonist*100, 2)*1000)
        if self.race_editor_energy_per_colonist > 0.01:
            c /= 2
        ap -= c+500
        """ caululate and aply the cost of reaserch stats """
        ap -= self.race_editor_starting_tech_level_in_energy**3*2 + self.race_editor_starting_tech_level_in_energy*3
        ap -= self.race_editor_starting_tech_level_in_weapons**3*2 + self.race_editor_starting_tech_level_in_weapons*3
        ap -= self.race_editor_starting_tech_level_in_propulsion**3*2 + self.race_editor_starting_tech_level_in_propulsion*3
        ap -= self.race_editor_starting_tech_level_in_construction**3*2 + self.race_editor_starting_tech_level_in_construction*3
        ap -= self.race_editor_starting_tech_level_in_electronics**3*2 + self.race_editor_starting_tech_level_in_electronics*3
        ap -= self.race_editor_starting_tech_level_in_biotechnology**3*2 + self.race_editor_starting_tech_level_in_biotechnology*3
        m = 0
        if self.race_editor_energy_research_cost_modifier > 100:
            m += self.race_editor_energy_research_cost_modifier/100 - 1
        elif self.race_editor_energy_research_cost_modifier < 100:
            m += self.race_editor_energy_research_cost_modifier/50 - 2 
        if self.race_editor_weapons_research_cost_modifier > 100:
            m += self.race_editor_weapons_research_cost_modifier/100 - 1
        elif self.race_editor_weapons_research_cost_modifier < 100:
            m += self.race_editor_weapons_research_cost_modifier/50 - 2
        if self.race_editor_propulsion_research_cost_modifier > 100:
            m += self.race_editor_propulsion_research_cost_modifier/100 - 1
        elif self.race_editor_propulsion_research_cost_modifier < 100:
            m += self.race_editor_propulsion_research_cost_modifier/50 - 2
        if self.race_editor_construction_research_cost_modifier > 100:
            m += self.race_editor_construction_research_cost_modifier/100 - 1
        elif self.race_editor_construction_research_cost_modifier < 100:
            m += self.race_editor_construction_research_cost_modifier/50 - 2
        if self.race_editor_electronics_research_cost_modifier > 100:
            m += self.race_editor_electronics_research_cost_modifier/100 - 1
        elif self.race_editor_electronics_research_cost_modifier < 100:
            m += self.race_editor_electronics_research_cost_modifier/50 - 2
        if self.race_editor_biotechnology_research_cost_modifier > 100:
            m += self.race_editor_biotechnology_research_cost_modifier/100 - 1
        elif self.race_editor_biotechnology_research_cost_modifier < 100:
            m += self.race_editor_biotechnology_research_cost_modifier/50 - 2
        ap -= -(m+1)*m*5 + -20*m
        self.race_editor_advantage_points_left = ap


RaceEditor.set_defaults(RaceEditor, __defaults)
#self.race_editor_advantege_points
