from . import game_engine
from .defaults import Defaults
from .game import Game
from .player import Player
from .star_system import StarSystem
from math import pi
from random import randint
from random import random
from .reference import ReferenceS


""" Default values (default, min, max)  """
__defaults = {
    'new_game_name': [''],
    'new_game_x': [500, 20, 2000], 
    'new_game_y': [500, 20, 2000], 
    'new_game_z': [200, 20, 2000], 
    'new_game_density': [95, 1, 100],
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
    'new_game_tech_tree': ['Inherit The Stars'],
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
        num_players = 0
        for i in range(1, 17):
            key = 'new_game_player{:02d}'.format(i)
            self.__dict__['options_' + key] = races
            if self.__dict__[key] != 'No Player':
                num_players += 1
        self.options_new_game_tech_tree = game_engine.load_list('tech_tree')
        # Create the game
        if action == 'create':
            systems = self.create_systems(self.calc_num_systems())
            homes = self.generate_home_systems(num_players, systems, self.new_game_player_distance)
            players = []
            for i in range(1, 17):
                race_name = self.__dict__['new_game_player{:02d}'.format(i)]
                if race_name != 'No Player':
                    # Protect against other objects in a race file
                    objs = game_engine.load('races', race_name, False)
                    for r in objs:
                        if r.__class__.__name__ == 'Race' and r.name == race_name:
                            players.append(Player(name=race_name, race=r))
            i = 0
            for s in systems:
                if s in homes:
                    s._create_system(Refecence(players[i]))
                else:
                    s._create_system(None)
            game = Game(name=self.new_game_name, players=players)
            game_engine.load('tech_tree', self.new_game_tech_tree)
            game_engine.save('games', self.new_game_name)

    def calc_num_systems(self):
        vx = self.new_game_x
        vy = self.new_game_y
        vz = self.new_game_z
        dimension = 3
        if self.new_game_x == 0 or self.new_game_x == 1:
            dimension -= 1
            vx = 2
        if self.new_game_y == 0 or self.new_game_y == 1:
            dimension -= 1
            vy = 2
        if self.new_game_z == 0 or self.new_game_z == 1:
            dimension -= 1
            vz = 2
        volume = ((4/3)*pi)*(vx/2)*(vy/2)*(vz/2)/(100**dimension)
        num_systems = round(volume * self.new_game_density)
        return num_systems

    def create_systems(self, num_systems):
        systems = []
        with open('stars/star_system.names') as file:
            names = []
            for name in file:
                names.append(name.strip())
        while len(systems) < num_systems:
            rx = (random() * 2) -1
            ry = (random() * 2) -1
            rz = (random() * 2) -1            
            distance = ((rx**2) + (ry**2) + (rz**2))**.5 
            if distance <= 1 and distance >= -1:
                rx = round(rx * (self.new_game_x/2))
                ry = round(ry * (self.new_game_y/2))
                rz = round(rz * (self.new_game_z/2))
                for s in systems:
                    counter = 0
                    if s.x == rx and s.y == ry and s.z == rz:
                        counter += 1
                        break
                    if counter == 100:
                        return 'too many systems'
                        break
                else:
                    counter = 0
                    system_name = names.pop(randint(0, len(names) - 1))
                    s = StarSystem(name=system_name, x=rx, y=ry, z=rz)
                    systems.append(s)
        return systems

    def generate_home_systems(self, num_players, systems, player_distance):
        home_systems = []
        home_systems.append(systems[0])
        if num_players == 1:
           pass 
        else:
            for i in systems:
                p = ''
                for k in home_systems:
                    if round((((i.x - k.x)**2) + ((i.y - k.y)**2) + ((i.z - k.z)**2))**.5) < player_distance or system.num_planets < 1:    
                        p += 'fail'
                    elif round((((i.x - k.x)**2) + ((i.y - k.y)**2) + ((i.z - k.z)**2))**.5) >= player_distance:
                          p += 'pass'
                if 'fail' not in p:
                    home_systems.append(i)
                if len(home_systems) == num_players:
                    break
                if i == systems[len(systems) - 1] and len(home_systems) < num_players:
                    player_distance *= .9
        return home_systems
            

NewGame.set_defaults(NewGame, __defaults)