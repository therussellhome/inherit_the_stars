import sys
from .playerui import PlayerUI
from ..race import Race, PRIMARY_RACE_TRAITS
from .. import game_engine


__defaults = {
    'options_race_editor_primary_race_trait': [PRIMARY_RACE_TRAITS],
    'race_editor_habitability_message': [''],
    'race_editor_file_to_load': [''],
    'options_race_editor_file_to_load': [[]],
    'race_editor_advantage_points_left': [0, -2000000, 2000000],
    'race_editor_screen_title': ['Race Editor'],
}


class RaceEditor(PlayerUI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        """List races for loading"""
        self.options_race_editor_file_to_load = game_engine.load_list('Race')
        self.options_race_editor_file_to_load.insert(0, '')
        race = Race()
        self.race_editor_screen_title = 'Race Editor'
        if self.player():
            race = self.player().race
            for key in Race.defaults:
                self['race_editor_' + key] = race[key]
            self.race_editor_screen_title = 'Race Viewer'
        elif self.race_editor_file_to_load != '':
            race = game_engine.load('Race', self.race_editor_file_to_load)
            for key in Race.defaults:
                self['race_editor_' + key] = race[key]
            self.race_editor_file_to_load = ''
        else:
            for key in Race.defaults:
                race[key] = self['race_editor_' + key]
        """ calculate and aply the cost of habitablility """
        self.race_editor_habitability_message = str(round(race.percent_planets_habitable(), 1)) \
            + '% of planets should be habitable for you'
        """validate that race has non-negative advantage points left"""
        self.race_editor_advantage_points_left = int(race.calc_points())
        if self.race_editor_advantage_points_left < 0:
            self.user_alerts.append(self.race_editor_name + ' has negative advantage points')
        elif action == 'save':
            game_engine.save('Race', race.name, race)


for key in Race.defaults:
    __defaults['race_editor_' + key] = Race.defaults[key]


RaceEditor.set_defaults(RaceEditor, __defaults, sparse_json=False)
