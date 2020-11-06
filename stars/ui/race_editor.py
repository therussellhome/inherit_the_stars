import sys
from math import log, exp
from ..race import Race
from ..defaults import Defaults
from .. import game_engine
#s = SUM(FILTER(C2:C80,E2:E80=Y1)) #total
#b = COUNTIFS(E28:E33, Y1)*2 #tech
#c = COUNTIFS(E40:E45, Y1)*2 #tech
#left = -s + (b+1)*(b/2)*10 - (c+1)*(c/2)*10
cost_of_growthrate = [-7091, -5673, -4256, -2839, -1422, -838, -403, -119, 40, 150, 201, 252, 303, 355, 406, 457, 509, 560, 611, 664]

__defaults = {
    'options_race_editor_primary_race_trait': [['Aku\'Ultani', 'Kender', 'Formics', 'Gaerhule', 'Halleyforms', 'Melconians', 'Pa\'anuri', 'Patryns', 'TANSTAAFL']],
    'race_editor_habitability_message': [''],
    'race_editor_file_to_load': [''],
    'options_race_editor_file_to_load': [[]],
    'race_editor_advantage_points_left': [0, -sys.maxsize, sys.maxsize],
}
def calc_habr_cost(start, stop): #not temperature
    size = stop - start + 1
    dis = abs((start+stop)/2 - 50)
    return (size*5 - 300) - dis*2


class RaceEditor(Defaults):

    """ calulate the cost of race traits """
    def calc_race_trait_cost(self):
        aps = 0
        lrts = 0
        if self.race_editor_primary_race_trait == 'Pa\'anuri':
            pass
        elif self.race_editor_primary_race_trait == 'Halleyforms':
            aps += 268
        elif self.race_editor_primary_race_trait == 'Formics':
            pass
        elif self.race_editor_primary_race_trait == 'Gaerhules':
            pass
        elif self.race_editor_primary_race_trait == 'Patryns':
            aps += 284
        elif self.race_editor_primary_race_trait == 'Melconians':
            aps += 176
        elif self.race_editor_primary_race_trait == 'TANSTAAFL':
            aps += 399
        elif self.race_editor_primary_race_trait == 'Kender':
            aps += 354
        elif self.race_editor_primary_race_trait == 'Aku\'Ultani':
            aps += 347
        if self.race_editor_lrt_Trader:
            aps += 126
            lrts += 1
            #print("T")
        if self.race_editor_lrt_Bioengineer:
            aps += 122
            lrts += 1
            #print("TT")
        if self.race_editor_lrt_SpacedOut:
            aps += 81
            lrts += 1
            #print("AD")
        if self.race_editor_lrt_WasteNot:
            aps += 76
            lrts += 1
            #print("UR")
        if self.race_editor_lrt_Hypermiler:
            aps += 66
            lrts += 1
            #print("IFE")
        if self.race_editor_lrt_McMansion:
            aps += 55
            lrts += 1
            #print("ISB")
        if self.race_editor_lrt_MadScientist:
            aps += -10
            lrts += 1
            #print("GR")
        if self.race_editor_lrt_QuickHeal:
            aps += -14
            lrts += 1
            #print("RS")
        if self.race_editor_lrt_BleedingEdge:
            aps += -28
            lrts += 1
            #print("BET")
        aps += -56
        if self.race_editor_lrt_Forager:
            aps += 56
            lrts += 1
            #print("NACE")
        #if self.race_editor_low_starting_popultion:
        #    aps += -62
        #    lrts += 1
        aps += -99
        if self.race_editor_lrt_2ndSight:
            aps += 99
            lrts += 1
            #print("NAS")
        if self.race_editor_lrt_JuryRigged:
            aps += -109
            lrts += 1
            #print("CE")
        #print(lrts)
        #print(aps)
        aps += (lrts+1) * lrts
        return aps

    def calc_reseach_cost(self):
        ap = 0
        ap -= self.race_editor_starting_tech_energy**3*2 + self.race_editor_starting_tech_energy*3
        ap -= self.race_editor_starting_tech_weapons**3*2 + self.race_editor_starting_tech_weapons*3
        ap -= self.race_editor_starting_tech_propulsion**3*2 + self.race_editor_starting_tech_propulsion*3
        ap -= self.race_editor_starting_tech_construction**3*2 + self.race_editor_starting_tech_construction*3
        ap -= self.race_editor_starting_tech_electronics**3*2 + self.race_editor_starting_tech_electronics*3
        ap -= self.race_editor_starting_tech_biotechnology**3*2 + self.race_editor_starting_tech_biotechnology*3
        m = 0
        if self.race_editor_research_modifier_energy > 100:
            m += self.race_editor_research_modifier_energy/100 - 1
        elif self.race_editor_research_modifier_energy < 100:
            m += self.race_editor_research_modifier_energy/50 - 2
        #print(m)
        if self.race_editor_research_modifier_weapons > 100:
            m += self.race_editor_research_modifier_weapons/100 - 1
        elif self.race_editor_research_modifier_weapons < 100:
            m += self.race_editor_research_modifier_weapons/50 - 2
        #print(m)
        if self.race_editor_research_modifier_propulsion > 100:
            m += self.race_editor_research_modifier_propulsion/100 - 1
        elif self.race_editor_research_modifier_propulsion < 100:
            m += self.race_editor_research_modifier_propulsion/50 - 2
        #print(m)
        if self.race_editor_research_modifier_construction > 100:
            m += self.race_editor_research_modifier_construction/100 - 1
        elif self.race_editor_research_modifier_construction < 100:
            m += self.race_editor_research_modifier_construction/50 - 2
        #print(m)
        if self.race_editor_research_modifier_electronics > 100:
            m += self.race_editor_research_modifier_electronics/100 - 1
        elif self.race_editor_research_modifier_electronics < 100:
            m += self.race_editor_research_modifier_electronics/50 - 2
        #print(m)
        if self.race_editor_research_modifier_biotechnology > 100:
            m += self.race_editor_research_modifier_biotechnology/100 - 1
        elif self.race_editor_research_modifier_biotechnology < 100:
            m += self.race_editor_research_modifier_biotechnology/50 - 2
        #print(m)
        try:
            ap -= -(((m*2+(m/abs(m)))*m*10) + abs(20*m))*(m/abs(m))
        except:
            pass
        #print(ap)
        return -ap

    def calc_economy_cost(self):
        ap = 0
        c = round((self.race_editor_colonists_to_operate_factory/1000)**(-0.5)*1000-1000)
        #print(c)
        ap -= c
        c = round((self.race_editor_colonists_to_operate_mine/1000)**(-0.5)*500-500)
        #print(c)
        ap -= c
        c = round((self.race_editor_colonists_to_operate_power_plant/1000)**(-0.5)*1000-1000)
        #print(c)
        ap -= c
        c = (1000/self.race_editor_colonists_to_operate_defense)*100-100
        #print(c)
        ap -= c
        c = round(log(self.race_editor_energy_per_colonist*0.1, 2)*1000)
        if self.race_editor_energy_per_colonist < 10:
            c /= 2
        #print(c)
        ap -= c+500
        #print(ap)
        ap -= (self.race_editor_starting_colonists-250)/1.25
        ap -= (10000-self.race_editor_cost_of_baryogenesis)/100
        return -ap

    def calc_hab_cost(self):
        ap = 0
        immunitys = 0
        if self.race_editor_hab_gravity_immune:
            immunitys += 1
            ap -= 400
        #    print('Yg')
        else:
        #    print(self.race_editor_hab_gravity, self.race_editor_hab_gravity_stop)
            ap -= calc_habr_cost(self.race_editor_hab_gravity, self.race_editor_hab_gravity_stop)
        #print(ap)
        if self.race_editor_hab_temperature_immune:
            immunitys += 1
            ap -= 450
        #    print('Yt')
        else:
        #    print(self.race_editor_hab_temperature, self.race_editor_hab_temperature_stop)
            size = self.race_editor_hab_temperature_stop - self.race_editor_hab_temperature + 1
            dis = abs((self.race_editor_hab_temperature + self.race_editor_hab_temperature_stop)/2 - 50)
            ap -= (size*5 - 300) - dis*4
        #print(ap)
        if self.race_editor_hab_radiation_immune:
            immunitys += 1
            ap -= 405
        #    print('Yr')
        else:
        #    print(self.race_editor_hab_radiation, self.race_editor_hab_radiation_stop)
            ap -= calc_habr_cost(self.race_editor_hab_radiation, self.race_editor_hab_radiation_stop)
        #print(ap)
        #print(immunitys)
        #print(self.race_editor_growth_rate)
        ap -= (immunitys*10 + 1) * (immunitys*5)
        #print(ap)
        ap -= cost_of_growthrate[self.race_editor_growth_rate-1]
        #print(ap)
        return -ap
    
    def calc_start_cost(self):
        ap = 0
        ap += self.race_editor_starting_factories*5-50
        ap += self.race_editor_starting_mines*3-30
        ap += self.race_editor_starting_power_plants*5-50
        ap += self.race_editor_starting_defenses*2-20
        ap += self.race_editor_starting_energy/1000-50
        ap += self.race_editor_starting_lithium/5-100
        ap += self.race_editor_starting_silicon/5-100
        ap += self.race_editor_starting_titanium/5-100
        return ap
    
    """ TODO """
    def _calc_habitability_message(self):
        overall_hab = 1.0
        if not self.race_editor_hab_gravity_immune:
            hab = 0.0
            for i in range(self.race_editor_hab_gravity, self.race_editor_hab_gravity_stop + 1):
                hab += (100.0 - i) * 2.0 / 101.0
            overall_hab *= hab / 100.0
        if not self.race_editor_hab_temperature_immune:
            hab = 0.0
            for i in range(self.race_editor_hab_temperature, self.race_editor_hab_temperature_stop + 1):
                hab += 1.7 * exp(-1.0 * (((i - 50.0) * (i - 50.0)) / (2.0 * 27.0 * 27.0))) - 0.1
            overall_hab *= hab / 100.0
        if not self.race_editor_hab_radiation_immune:
            hab = 0.0
            for i in range(self.race_editor_hab_radiation, self.race_editor_hab_radiation_stop + 1):
                hab += 100.0/101.0
            overall_hab *= hab / 100.0
        overall_hab = 100.0 * max(overall_hab, 0.001)
        self.race_editor_habitability_message = str(round(overall_hab, 1)) + '% of planets should be habitable for you'

    def post(self, action):
        if action == 'reset':
            self.reset_to_default()
        # List races for loading
        self.options_race_editor_file_to_load = game_engine.load_list('races')
        self.options_race_editor_file_to_load.insert(0, '')
        if self.race_editor_file_to_load != '':
            objs = game_engine.load('races', self.race_editor_file_to_load, False)
            # populate self
            for r in objs:
                if r.__class__.__name__ == 'Race' and r.name == self.race_editor_file_to_load:
                    for key in Race.defaults:
                        setattr(self, 'race_editor_' + key, getattr(r, key))
            self.race_editor_file_to_load = ''
        """ aply the cost of race traits """
        ap = 1000 - self.calc_race_trait_cost()
        """ calculate and aply the cost of habitablilaty """
        self._calc_habitability_message()
        if self.race_editor_hab_gravity_immune:
            self.race_editor_hab_gravity = 0
            self.race_editor_hab_gravity_stop = 100
        if self.race_editor_hab_temperature_immune:
            self.race_editor_hab_temperature = 0
            self.race_editor_hab_temperature_stop = 100
        if self.race_editor_hab_radiation_immune:
            self.race_editor_hab_radiation = 0
            self.race_editor_hab_radiation_stop = 100
        ap -= self.calc_hab_cost()
        """ calulate and aply the cost of the econimy """
        ap -= self.calc_economy_cost()
        """ caululate and aply the cost of reaserch stats """
        ap -= self.calc_reseach_cost()
        """ caululate and aply the cost of what you start with """
        ap -= self.calc_start_cost()
        self.race_editor_advantage_points_left = int(ap)
        self.options_race_editor_file_to_load = game_engine.load_list('races')
        if action == 'save':
            r = Race()
            for key in Race.defaults:
                setattr(r, key, getattr(self, 'race_editor_' + key))
            game_engine.save('races', self.race_editor_name, r)


for key in Race.defaults:
    __defaults['race_editor_' + key] = Race.defaults[key]

RaceEditor.set_defaults(RaceEditor, __defaults)