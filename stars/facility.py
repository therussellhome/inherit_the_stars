import sys
from .tech import Tech
from .scanner import Scanner


""" Default values (default, min, max)  """
__defaults = {
    'tech': [Tech()],
    'quantity': [0, 0, sys.maxsize],

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
        super().__init__(**kwargs)

    def colonize(self, tech):
        if self.quantity == 0:
            self.tech = tech
        self.quantity += 1


Facility.set_defaults(Facility, __defaults)
