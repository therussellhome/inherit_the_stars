import sys
from pathlib import Path
from . import game_engine

""" Default values (default, min, max)  """
__defaults = {
    'open_game_list': [''],
    'options_open_game_list': [[]],
    'open_game_auto': [True],
    'open_game_player01': ['No Player'],
    'open_game_player01_status': [''],
    'open_game_player02': ['No Player'],
    'open_game_player02_status': [''],
    'open_game_player03': ['No Player'],
    'open_game_player03_status': [''],
    'open_game_player04': ['No Player'],
    'open_game_player04_status': [''],
    'open_game_player05': ['No Player'],
    'open_game_player05_status': [''],
    'open_game_player06': ['No Player'],
    'open_game_player06_status': [''],
    'open_game_player07': ['No Player'],
    'open_game_player07_status': [''],
    'open_game_player08': ['No Player'],
    'open_game_player08_status': [''],
    'open_game_player09': ['No Player'],
    'open_game_player09_status': [''],
    'open_game_player10': ['No Player'],
    'open_game_player10_status': [''],
    'open_game_player11': ['No Player'],
    'open_game_player11_status': [''],
    'open_game_player12': ['No Player'],
    'open_game_player12_status': [''],
    'open_game_player13': ['No Player'],
    'open_game_player13_status': [''],
    'open_game_player14': ['No Player'],
    'open_game_player14_status': [''],
    'open_game_player15': ['No Player'],
    'open_game_player15_status': [''],
    'open_game_player16': ['No Player'],
    'open_game_player16_status': ['']
}

""" Represent Open Game action """
class OpenGame(game_engine.Defaults):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)
        game_dir = Path.home() / 'stars' / 'games'
        for p in game_dir.iterdir():
            self.options_open_game_list.append(p.name[0:-4])
        if 'submit' in kwargs:
            game_engine.load_game(self.open_game_list)

# Register the class with the game engine
game_engine.register(OpenGame, defaults=__defaults)
