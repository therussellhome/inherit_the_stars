import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'energy': [0, 0, sys.maxsize],
    'weapons': [0, 0, sys.maxsize],
    'propulsion': [0, 0, sys.maxsize],
    'construction': [0, 0, sys.maxsize],
    'electronics': [0, 0, sys.maxsize],
    'biotechnology': [0, 0, sys.maxsize]
}

""" Represent 'tech level' """
class TechLevel(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ Determine if the item is available for a player's tech level """
    def is_available(self, player_level):
        if player_level.energy <= self.energy and player_level.weapons <= self.weapons and player_level.propulsion <= self.propulsion and player_level.construction <= self.construction and player_level.electronics <= self.electronics and player_level.biotechnology <= self.biotechnology:
            return True
        return False

    def __add__(self, other):
        t = TechLevel()
        t.energy = max(self.energy, other.energy)
        t.weapons = max(self.weapons, other.weapons)
        t.propulsion = max(self.propulsion, other.propulsion)
        t.construction = max(self.construction, other.construction)
        t.electronics = max(self.electronics, other.electronics)
        t.biotechnology = max(self.biotechnology, other.biotechnology)
        return t

TechLevel.set_defaults(TechLevel, __defaults)
