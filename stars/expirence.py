from .defaults import Defaults

__defaults = {
    'comishoning_date': [0.0, 0.0, 2**128],
    'base_expirence': [0.0, 0.0, 10.0],
    'battle_expirence': [0.0, 0.0, 2**128*100],
}

class Expirence(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        
    def calc(self, date):
        return self.base_expirence + self.comishoning_date - date + self.battle_expirence

Expirence.set_defaults(Expirence, __defaults)
