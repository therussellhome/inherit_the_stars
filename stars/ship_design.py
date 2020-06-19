import sys
from . import game_engine
from .defaults import Defaults
from .reference import Reference


""" Default values (default, min, max)  """
__defaults = {
    'hull': [ShipHull()],
    'components': [[]],
    'player': [Reference()],
}



class ShipDesign(Defaults):
    """ Initialize defaults """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        game_engine.register(self)
    def get_armor_strength(self):
        a = self.hull.armor
        for c in self.compontent:
            a += c.armor
        return a
    def get_shield_strength(self):
        b = self.hull.shield
        for s in self.component:
            b += s.shield
        return b
    def get_cargo_max(self):
        d = self.hull.cargo
        for c in self.component:
            d += c
        return d
    def get_fuel_max(self):
        e = self.hull.fuel
        for f in self.component:
            e += f
        return e



