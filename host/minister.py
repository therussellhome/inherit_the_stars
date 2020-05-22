import sys
from . import game_engine

""" Default values (default, min, max)  """
__defaults = {
    'power_plants': [25, 0, 100],
    'factories': [25, 0, 100],
    'mines': [25, 0, 100],
    'defenses': [25, 0, 100],
    'build_scanner_after_num_facilitys': [50, 0, sys.maxsize],
    'build_penetrating_after_num_facilitys': [100, 0, sys.maxsize],
    'build_mattrans_after_num_facilitys': [100, 0, sys.maxsize],
    'build_min_terraform': [1, 0, 100],
    'build_max_terraform': [100, 0, 100]
}

""" TODO """
class Minister(game_engine.Defaults):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)
        if 'name' not in kwargs:
            self.name = 'minister_' + str(id(self))
        # do not register the object as it is stored by the player object
    
    """ makes shure that all effort is alocated and the total is = to 100% """
    def __getattribute__(self, name):
        power_plants = super().__getattribute__('power_plants')
        factories = super().__getattribute__('factories')
        mines = super().__getattribute__('mines')
        defenses = super().__getattribute__('defenses')
        factor = power_plants + factories + mines + defenses
        if factor != 0:
            factor = 100 / factor
        factories = int(factories * factor)
        mines = int(mines * factor)
        defenses = int(defenses * factor)
        self.power_plants = 100 - factories - mines - defenses
        self.factories = factories
        self.mines = mines
        self.defenses = defenses
        return super().__getattribute__(name)

game_engine.register(Minister, defaults=__defaults)
