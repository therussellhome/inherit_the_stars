from .defaults import Defaults
from sys import maxsize

__defaults = {
    'comishoning_date': [0.0, 0.0, maxsize],
    'base_expirence': [0.0, 0.0, maxsize],
    'battle_expirence': [0.0, 0.0, maxsize],
}

class Expirence(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        
    def calc(self, date):
        return self.base_expirence + self.comishoning_date - date + self.battle_expirence

Expirence.set_defaults(Expirence, __defaults)
