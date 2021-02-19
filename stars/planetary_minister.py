import sys
from .defaults import Defaults


""" Default values (default, min, max)  """
__defaults = {
    'name': '@UUID',
    'new_colony_minister': False,
    'allow_baryogenesis': True,
    'max_terraform': False,
    'planets': [],
    'name': 'newbie',
    'color': 'purple',
    # percent population operating each falicity type where the key matches the facility types
    'power_plants': (30, 0, 100),
    'factories': (30, 0, 100),
    'mines': (30, 0, 100),
    'defenses': (10, 0, 100),
}


""" The planetary minister controls the planetary construction phase of turn generation """
class PlanetaryMinister(Defaults):
    """ makes shure that all effort is alocated and the total is = to 100% """
    def normalize(self):
        factor = self.power_plants + self.factories + self.mines + self.defenses
        if factor != 0:
            factor = 100 / factor
        self.defenses = int(self.defenses * factor)
        self.factories = int(self.factories * factor)
        self.mines = int(self.mines * factor)
        # give any surplus to power plants
        self.power_plants = 100 - self.defenses - self.factories - self.mines


PlanetaryMinister.set_defaults(PlanetaryMinister, __defaults)
