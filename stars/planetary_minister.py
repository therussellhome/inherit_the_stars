import sys
from .defaults import Defaults

""" Default values (default, min, max)  """
__defaults = {
    'new_colony_minister': [False],
    'build_scanner_after_num_facilities': [50, 0, sys.maxsize],
    'build_penetrating_after_num_facilities': [100, 0, sys.maxsize],
    'build_mattrans_after_num_facilities': [100, 0, sys.maxsize],
    'build_min_terraform': [1, 0, 100],
    'build_max_terraform': [100, 0, 100],
    'allow_baryogenesis': [True],
    'planets': [[]],
    # facilities where the key matches the tech category
    'Power Plant': [25, 0, 100],
    'Factory': [25, 0, 100],
    'Mineral Extractor': [25, 0, 100],
    'Planetary Shield': [25, 0, 100],
}


""" TODO """
class PlanetaryMinister(Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'name' not in kwargs:
            self.name = 'Planetary Minister ' + str(id(self))
    
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
