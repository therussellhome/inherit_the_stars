import sys
from math import pi
from random import randint
from random import random
from .. import game_engine
from ..defaults import Defaults
from ..game import Game
from ..location import rand_location
from ..player import Player
from ..race import Race
from ..reference import Reference
from ..star_system import StarSystem
from ..tech import Tech


""" Default values (default, min, max)  """
__defaults = {
    'new_game_name': [''],
    'new_game_num_systems': [0, 0, sys.maxsize],
    'new_game_x': [500, 100, 2000], 
    'new_game_y': [500, 100, 2000], 
    'new_game_z': [500, 0, 2000], 
    'new_game_density': [8, 1, 100],
    'new_game_player_distance': [200, 1, 2000],
    'new_game_player01': ['No Player'],
    'new_game_player02': ['No Player'],
    'new_game_player03': ['No Player'],
    'new_game_player04': ['No Player'],
    'new_game_player05': ['No Player'],
    'new_game_player06': ['No Player'],
    'new_game_player07': ['No Player'],
    'new_game_player08': ['No Player'],
    'new_game_player09': ['No Player'],
    'new_game_player10': ['No Player'],
    'new_game_player11': ['No Player'],
    'new_game_player12': ['No Player'],
    'new_game_player13': ['No Player'],
    'new_game_player14': ['No Player'],
    'new_game_player15': ['No Player'],
    'new_game_player16': ['No Player'],
    'options_new_game_player01': [[]],
    'options_new_game_player02': [[]],
    'options_new_game_player03': [[]],
    'options_new_game_player04': [[]],
    'options_new_game_player05': [[]],
    'options_new_game_player06': [[]],
    'options_new_game_player07': [[]],
    'options_new_game_player08': [[]],
    'options_new_game_player09': [[]],
    'options_new_game_player10': [[]],
    'options_new_game_player11': [[]],
    'options_new_game_player12': [[]],
    'options_new_game_player13': [[]],
    'options_new_game_player14': [[]],
    'options_new_game_player15': [[]],
    'options_new_game_player16': [[]],
    'new_game_public_player_scores': [30, 0, 200], 
    'new_game_victory_after': [50, 10, 200], 
    'new_game_victory_conditions': [1, 1, 10], 
    'new_game_victory_enemies': [True],
    'new_game_victory_enemies_left': [0, 0, 15], 
    'new_game_victory_score': [True],
    'new_game_victory_score_number': [1000, 100, 10000], 
    'new_game_victory_tech': [True],
    'new_game_victory_tech_levels': [100, 10, 300], 
    'new_game_victory_planets': [True],
    'new_game_victory_planets_number': [200, 50, 1000], 
    'new_game_victory_energy': [True],
    'new_game_victory_energy_number': [10000, 1000, 100000], 
    'new_game_victory_minerals': [True],
    'new_game_victory_minerals_number': [10000, 1000, 100000], 
    'new_game_victory_production': [True],
    'new_game_victory_production_number': [10000, 1000, 100000], 
    'new_game_victory_ships': [True],
    'new_game_victory_ships_number': [1000, 100, 10000], 
    'new_game_victory_shipsofthewall': [True],
    'new_game_victory_shipsofthewall_number': [150, 50, 1000], 
    'new_game_victory_starbases': [True],
    'new_game_victory_starbases_number': [25, 10, 100], 
    'new_game_tech_tree': ['Default'],
    'options_new_game_tech_tree': [[]],
}


""" Represent Open Game action """
class NewGame(Defaults):
    """ Interact with UI """
    def post(self, action):
        if action == 'reset':
            self.reset_to_default()
        # Always refresh the list of races
        races = game_engine.load_list('races')
        races.insert(0, 'No Player')
        players = []
        for i in range(1, 17):
            key = 'new_game_player{:02d}'.format(i)
            self.__dict__['options_' + key] = races
            if self.__dict__[key] != 'No Player':
                players.append(self.__dict__[key])
        self.options_new_game_tech_tree = game_engine.load_list('tech_tree')
        self.options_new_game_tech_tree.insert(0, 'Default')
        self.new_game_num_systems = self.calc_num_systems(self.new_game_x, self.new_game_y, self.new_game_z, self.new_game_density)
        # Create the game
        if action == 'create' and len(players) > 0:
            game = Game(name=self.new_game_name)
            game_engine.register(game)
            # Load tech tree
            tech_tree = []
            if self.new_game_tech_tree == 'Default':
                tech = game_engine.load_defaults('Tech')
            else:
                tech = game_engine.load('tech_tree', self.new_game_tech_tree)
            # Protect against other objects in a tech tree file
            for t in tech:
                if isinstance(t, Tech):
                    tech_tree.append(t)
            # Create empty systems
            system_names = []
            with open('stars/star_system.names') as file:
                for name in file:
                    system_names.append(name.strip())
            game.systems = self.create_systems(self.new_game_num_systems, system_names, self.new_game_x, self.new_game_y, self.new_game_z)
            # Create players and their home systems
            player_objs = []
            homes = self.generate_home_systems(len(players), game.systems, self.new_game_player_distance)
            for i in range(0, len(players)):
                # Protect against other objects in a race file
                r = game_engine.load('races', players[i])
                if isinstance(r, Race) and r.name == players[i]:
                    p = Player(race=r, tech=tech_tree)
                    homes[i].create_system(Reference(p))
                    game.players.append(p)
                else:
                    print('reject ', players[i])
            # Create planets in systems
            for s in game.systems:
                if not s in homes:
                    s.create_system()
            game_engine.save('host', game.name, game)
            for p in game.players:
                game_engine.save('games', game.name + ' - ' + p.name, p)

    """ Calculate the number of systems based on the size and density """
    def calc_num_systems(self, x, y, z, density):
        dimension = 3
        if z < 2:
            dimension = 2
            z = 2
        # compute volume in light centuries
        volume = ((4/3) * pi) * (x/2) * (y/2) * (z/2) / (100**dimension)
        return round(volume * density)

    """ Create the systems """
    def create_systems(self, num_systems, names, x, y, z):
        systems = []
        attempt = 0
        while len(systems) < num_systems and len(names) > 0 and attempt < 1000:
            l = rand_location(x / 2, y / 2, z / 2)
            for s in systems:
                if s.location - l < 4.0:
                    attempt += 1
                    break
            else:
                attempt = 0
                system_name = names.pop(randint(0, len(names) - 1))
                s = StarSystem(name=system_name, location=l)
                systems.append(s)
        return systems

    """ Select planets to be home systems """
    def generate_home_systems(self, num_players, systems, player_distance):
        if len(systems) < num_players:
            return []
        home_systems = [systems[0]]
        while len(home_systems) < num_players:
            for s in systems:
                for h in home_systems:
                    if s == h or s.location - h.location <= player_distance:
                        break
                else:
                    home_systems.append(s)
                    if len(home_systems) == num_players:
                        break
            else:
                player_distance = player_distance * 0.9 - 1
        return home_systems
            

NewGame.set_defaults(NewGame, __defaults)
