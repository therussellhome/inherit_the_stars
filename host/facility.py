import sys
import game_engine
from tech import Tech
from scanner import Scanner


""" Default values (default, min, max)  """
__defaults = {
    'upgrade_path': [''],
    'upgrade_level': [0, 0, 100],
    'output_per_facility': [0.0, 0.0, sys.maxsize],
    'effort_per_facility': [1000, 1, sys.maxsize],
    'defense': [0, 0, 100],
    'scanner': [Scanner()],
    'mineral_depletion_rate': [0, 0, 100],
    'mat_trans_energy': [0, 0, sys.maxsize]
}

""" Represent 'minerals' """
class Facility(Tech):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)

# Register the class with the game engine
game_engine.register(Facility, defaults=__defaults)
