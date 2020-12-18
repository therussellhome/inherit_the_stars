import sys
from .defaults import Defaults

""" Default values (default, min, max)  """
__defaults = {
    'new_colony_minister': [False],
    'allow_baryogenesis': [True],
    'max_terraform': [False],
    'planets': [[]],
    'name': ['newbie'],
    # facilities where the key matches the tech category
    'Power Plant': [25, 0, 100],
    'Factory': [25, 0, 100],
    'Mineral Extractor': [25, 0, 100],
    'Planetary Shield': [25, 0, 100],
    'color': ['purple'],
}


""" TODO """
class PlanetaryMinister(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    """ makes shure that all effort is alocated and the total is = to 100% """
    def normalize(self):
        power_plants = getattr(self, 'Power Plant')
        factories = getattr(self, 'Factory')
        mines = getattr(self, 'Mineral Extractor')
        defenses = getattr(self, 'Planetary Shield')
        factor = power_plants + factories + mines + defenses
        if factor != 0:
            factor = 100 / factor
        factories = int(factories * factor)
        mines = int(mines * factor)
        defenses = int(defenses * factor)
        setattr(self, 'Power Plant', 100 - factories - mines - defenses)
        setattr(self, 'Factory', factories)
        setattr(self, 'Mineral Extractor', mines)
        setattr(self, 'Planetary Shield', defenses)


PlanetaryMinister.set_defaults(PlanetaryMinister, __defaults)
