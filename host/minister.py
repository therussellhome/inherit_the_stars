import game_engine

""" Default values (default, min, max)  """
__defaults = {
    'power_plants': [20, 0, 100],
    'factories': [20, 0, 100],
    'mines': [20, 0, 100],
    'defenses': [20, 0, 100],
    'research': [20, 0, 100]
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
        research = super().__getattribute__('research')
        factor = power_plants + factories + mines + defenses + research
        if factor != 0:
            factor = 100 / factor
        power_plants = int(power_plants * factor)
        factories = int(factories * factor)
        mines = int(mines * factor)
        defenses = int(defenses * factor)
        self.power_plants = power_plants
        self.factories = factories
        self.mines = mines
        self.defenses = defenses
        self.research = 100 - power_plants - factories - mines - defenses
        return super().__getattribute__(name)

game_engine.register(Minister, defaults=__defaults)

def _test():
    print('minister._test - begin')
    _test_init()
    _test_edit()
    print('minister._test - end')

def _test_edit():
    print('minister._test_edit - begin')
    minister = Minister(name='Test_Minister')
    minister.power_plants = 30
    minister.factories = 50
    minister.mines = 260
    minister.defenses = 30
    minister.research = 30
    if minister.power_plants != 12: print('minister._test_edit power_plants ', minister.power_plants)
    if minister.factories != 20: print('minister._test_edit factories', minister.factories)
    if minister.mines != 41: print('minister._test_edit mines', minister.mines)
    if minister.defenses != 12: print('minister._test_edit defenses', minister.defenses)
    if minister.research != 15: print('minister._test_edit research', minister.research)
    print('minister._test_edit - end')

def _test_init():
    print('minister._test_init - begin')
    minister = Minister(name='Test_Mineister')
    if minister.power_plants != 20 and minister.factories != 20 and minister.mines != 20 and minister.defenses != 20 and minister.research != 20:
        print('init fail')
    print('minister._test___init__ - end')
