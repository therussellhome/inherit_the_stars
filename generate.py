#!/usr/bin/python3

import sys
from stars import *


game = game_engine.load('Game', sys.argv[1])
if game == None:
    print('Could not load game', sys.argv[1])
else:
    game.new_turn()
