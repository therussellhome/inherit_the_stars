import sys
from ..race import Race
from ..defaults import Defaults
from .. import game_engine

__defaults = {
    'options_race_editor_primary_race_trait': [['Aku\'Ultani', 'Kender', 'Formics', 'Gaerhule', 'Halleyforms', 'Melconians', 'Pa\'anuri', 'Patryns', 'TANSTAAFL']],
    'race_editor_habitability_message': [''],
    'race_editor_file_to_load': [''],
    'options_race_editor_file_to_load': [[]],
    'race_editor_advantage_points_left': [0, -2000000, 2000000],
}

class RaceEditor(Defaults):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        if action == 'reset':
            self.reset_to_default()
        """List races for loading"""
        self.options_race_editor_file_to_load = game_engine.load_list('races')
        self.options_race_editor_file_to_load.insert(0, '')
        if self.race_editor_file_to_load != '':
            objs = [game_engine.load('races', self.race_editor_file_to_load)]
            """populate self"""
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
        """validate that race has non-negative advantage points left"""
        self.race_editor_advantage_points_left = int(race.calc_points())
        if action == 'save':
            if self.race_editor_advantage_points_left < 0:
                print("INVALID RACE")
            else:
                game_engine.save('races', race.name, race)

    
for key in Race.defaults:
    __defaults['race_editor_' + key] = Race.defaults[key]


RaceEditor.set_defaults(RaceEditor, __defaults)
