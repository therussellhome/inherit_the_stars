import sys
from math import log, exp
from ..race import Race
from ..defaults import Defaults
from .. import game_engine
#s = SUM(FILTER(C2:C80,E2:E80=Y1)) #total
#b = COUNTIFS(E28:E33, Y1)*2 #tech
#c = COUNTIFS(E40:E45, Y1)*2 #tech
#left = -s + (b+1)*(b/2)*10 - (c+1)*(c/2)*10



__defaults = {
    'options_race_editor_primary_race_trait': [['Aku\'Ultani', 'Kender', 'Formics', 'Gaerhule', 'Halleyforms', 'Melconians', 'Pa\'anuri', 'Patryns', 'TANSTAAFL']],
    'race_editor_habitability_message': [''],
    'race_editor_file_to_load': [''],
    'options_race_editor_file_to_load': [[]],
    'race_editor_advantage_points_left': [0, -sys.maxsize, sys.maxsize],
}

#cost_of_growthrate = [-7091, -5673, -4256, -2839, -1422, -838, -403, -119, 40, 150, 201, 252, 303, 355, 406, 457, 509, 560, 611, 664]

class RaceEditor(Defaults):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if action == 'reset':
            self.reset_to_default()
        # List races for loading
        self.options_race_editor_file_to_load = game_engine.load_list('races')
        self.options_race_editor_file_to_load.insert(0, '')
        if self.race_editor_file_to_load != '':
            objs = [game_engine.load('races', self.race_editor_file_to_load)]
            # populate self
            for r in objs:
                if r.__class__.__name__ == 'Race' and r.name == self.race_editor_file_to_load:
                    for key in Race.defaults:
                        setattr(self, 'race_editor_' + key, getattr(r, key))
            self.race_editor_file_to_load = ''
        race = Race()
        for key in Race.defaults:
            setattr(race, key, getattr(self, 'race_editor_' + key))

        """ calculate and aply the cost of habitablility """
        self.race_editor_habitability_message = str(round(race.percent_planets_habitable(), 1)) \
            + '% of planets should be habitable for you'
        if self.race_editor_hab_gravity_immune:
            self.race_editor_hab_gravity = 0
            self.race_editor_hab_gravity_stop = 100
        if self.race_editor_hab_temperature_immune:
            self.race_editor_hab_temperature = 0
            self.race_editor_hab_temperature_stop = 100
        if self.race_editor_hab_radiation_immune:
            self.race_editor_hab_radiation = 0
            self.race_editor_hab_radiation_stop = 100
        #ap -= self.calc_hab_cost()
        #""" calulate and aply the cost of the economy """
        #ap -= self.calc_economy_cost()
        #""" caululate and aply the cost of reaserch stats """
        #ap -= self.calc_research_cost()
        #""" caululate and aply the cost of what you start with """
        #ap -= self.calc_start_cost()
        self.race_editor_advantage_points_left = int(ap)
        self.options_race_editor_file_to_load = game_engine.load_list('races')
        if action == 'save':
            game_engine.save('races', self.race_editor_name, r)

    
    """ calulate the cost of race traits """
    #def calc_race_trait_cost(self):
    #    aps = 0
    #    lrts = 0
    #    if self.race_editor_primary_race_trait == 'Pa\'anuri':
    #        pass
        #print(lrts)
        #print(aps)
        #aps += (lrts+1) * lrts
        #return aps


    #def calc_economy_cost(self):

    #def calc_hab_cost(self):
    
for key in Race.defaults:
    __defaults['race_editor_' + key] = Race.defaults[key]


RaceEditor.set_defaults(RaceEditor, __defaults)
