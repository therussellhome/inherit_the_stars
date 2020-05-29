from . import game_engine
from .defaults import Defaults
from . import star_system
from random import randint
from random import random
from math import pi


""" Default values (default, min, max)  """
__defaults = {
    'new_game_name': [''],
    'new_game_x': [100, 1, 100], 
    'new_game_y': [100, 1, 100], 
    'new_game_z': [100, 1, 100], 
    'new_game_density': [95, 1, 100],
    'new_game_player_distance': [15, 1, 50],
    'new_game_public_player_scores': [True], 
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
    'new_game_victory_tech': [True],
    'new_game_victory_tech_level': [20, 1, 50], 
    'new_game_victory_tech_level_in_fields': [4, 1, 6], 
    'new_game_number_of_ships': [300, 1, 500], 
    'new_game_number_of_planets': [75, 1, 200], 
    'new_game_number_of_factories': [200, 1, 500], 
    'new_game_number_of_power_plants': [200, 1, 500], 
    'new_game_number_of_mines': [200, 1, 500], 
    'new_game_number_of_other_players_left': [0, 0, 15], 
    'new_game_number_of_conditions_met': [1, 1, 9], 
    'new_game_years_till': [75, 1, 200], 
}


""" Represent Open Game action """
class NewGame(Defaults):
    """ Interact with UI """
    def post(self, action, **kwargs):
        self.__dict__.update(kwargs)
        if action == 'reset':
            self.reset_to_default()
        # Always refresh the list of games
        races = game_engine.load_list('races')
        races.insert(0, 'No Player')
        for i in range(1, 17):
            key = 'options_new_game_player{:02d}'.format(i)
            self.__dict__[key] = races
        # Create the game
        if action == 'submit':
            self.create_systems(self.calc_num_systems())
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
                    s = star_system.StarSystem(name=system_name, x=rx, y=ry, z=rz)
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
                    if round((((i.x - k.x)**2) + ((i.y - k.y)**2) + ((i.z - k.z)**2))**.5) < player_distance:    
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
