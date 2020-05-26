from . import game_engine
from .defaults import Defaults 


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
    def post(self, action):
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
            pass
            

NewGame.set_defaults(NewGame, __defaults)
