import sys
from math import pi
from random import randint
from random import random
from .. import game_engine
from ..defaults import Defaults
from ..game import Game
from ..player import Player
from ..race import Race
from ..reference import Reference
from ..star_system import StarSystem
from ..tech import Tech
from .ui import UI


""" Default values (default, min, max)  """
__defaults = {
    'new_game_name': '',
    'new_game_players': [],
    'new_game_x': (500, 0, 10000), 
    'new_game_y': (500, 0, 10000), 
    'new_game_z': (500, 0, 10000), 
    'new_game_num_systems': (1000, 50, sys.maxsize),
    'new_game_public_player_scores': (30, 0, 200), 
    'new_game_victory_after': (50, 10, 200), 
    'new_game_victory_conditions': (1, 1, 10), 
    'new_game_victory_enemies_left': (0, -1, 15), 
    'new_game_victory_score_number': (1000, -100, 10000), 
    'new_game_victory_tech_levels': (100, -10, 300), 
    'new_game_victory_planets_number': (200, -10, 1000), 
    'new_game_victory_energy_number': (10000, -1000, 100000), 
    'new_game_victory_minerals_number': (10000, -1000, 100000), 
    'new_game_victory_production_number': (10000, -1000, 100000), 
    'new_game_victory_ships_number': (1000, -100, 10000), 
    'new_game_victory_shipsofthewall_number': (150, -50, 1000), 
    'new_game_victory_starbases_number': (25, -10, 100), 
    'new_game_tech_tree': 'Inherit the Stars!',
    'options_new_game_tech_tree': [],
    'new_game_system_names': 'Inherit the Stars!',
    'options_new_game_system_names': [],
}


""" Represent Open Game action """
class NewGame(UI):
    def __init__(self, action, **kwargs):
        super().__init__(**kwargs)
        # Always refresh the list of races
        races = game_engine.load_list('Race')
        last_found = -1
        self.new_game_players = []
        player_races = []
        for i in range(0, 999):
            key = 'new_game_player{:02d}'.format(i)
            if getattr(self, key, '') != '':
                r = game_engine.load('Race', self[key])
                if not isinstance(r, Race):
                    self.user_alerts.append('File does not contain a race: ' + self[key])
                    #TODO these need to pop-up on the gui
                elif r.calc_points() < 0:
                    self.user_alerts.append('Race has negative advantage points: ' + self[key])
                else:
                    player_races.append(r)
                    self.new_game_players.append(self._races(key, races))
                    last_found = i
        key = 'new_game_player{:02d}'.format(last_found + 1)
        self[key] = ''
        self.new_game_players.append(self._races(key, races))
        self.new_game_num_systems = max(len(player_races), self.new_game_num_systems)
        self.options_new_game_tech_tree = game_engine.load_list('Tech')
        self.options_new_game_system_names = game_engine.load_list('StarSystems')
        # Load the system names
        system_names = game_engine.load('StarSystems', self.new_game_system_names)
        self.new_game_num_systems = min(self.new_game_num_systems, len(system_names))
        # Create the game
        if action == 'create' and len(player_races) > 0:
            game = Game(self.new_game_x, self.new_game_y, self.new_game_z, self.new_game_num_systems, system_names, ID=self.new_game_name, races=player_races, tech_file=self.new_game_tech_tree)
            game.save()

    def _races(self, key, races):
        select = '<td><select id="' + key + '" class="hfill" onchange="post(\'new_game\')"><option></option>'
        for r in races:
            select += '<option'
            if r == self[key]:
                select += ' selected="true"'
            select += '>' + r + '</option>'
        select += '</select></td>'
        return select


NewGame.set_defaults(NewGame, __defaults, sparse_json=False)
