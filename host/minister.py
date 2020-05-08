import game_engine

""" Default values (default, min, max)  """
__defaults = {
    'power_plants': [0.0, 0.0, 100.0],
    'factories': [0.0, 0.0, 100.0],
    'mines': [0.0, 0.0, 100.0],
    'defences': [0.0, 0.0, 100.0],
    'research': [0.0, 0.0, 100.0],
    'name': ["Unnamed Minister"]
}

""" TODO """
class Minister(game_engine.Defaults):
    def __init__(self, **kwargs):
        super()._apply_defaults(**kwargs)
        self.check_range()
        game_engine.register(self)
    
    """ lets you edit the ministers ratios """
    def edit(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
        self.check_range()
    
    """ makes shure that all effort is alocated and the total is = to 100% """
    def check_range(self):
        if self.power_plants == 0 and self.factories == 0 and self.mines == 0 and self.defences == 0 and self.research == 0:
            self.power_plants = 1
            self.factories = 1
            self.mines = 1
            self.defences = 1
            self.research = 1
        total = (self.power_plants + self.factories + self.mines + self.defences + self.research)
        if total != 100:
            self.power_plants = self.power_plants * 100/total
            self.factories = self.factories * 100/total
            self.mines = self.mines * 100/total
            self.defences = self.defences * 100/total
            self.research = self.research * 100/total

game_engine.register(Minister, defaults=__defaults)

""" TODO """
def _test():
    print('minister._test - begin')
    _test_init()
    _test_edit()
    print('minister._test - end')

""" Tests the .edit function """
def _test_edit():
    print('minister._test_edit - begin')
    minister = Minister(name='Test_Minister')
    minister.edit(power_plants=30, factories=50, mines=200, defences=30, research=30)
    if round(minister.power_plants, 1) != 12.5 or round(minister.factories, 1) != 20.8 or round(minister.mines, 1) != 41.7 or round(minister.defences, 1) != 12.5 or round(minister.research, 1) != 12.5:
        print('edit fail', round(minister.power_plants, 1), round(minister.factories, 1), round(minister.mines, 1), round(minister.defences, 1), round(minister.research, 1))
        print('edit fail', minister.power_plants, minister.factories, minister.mines, minister.defences, minister.research)
    print('minister._test_edit - end')

""" tests the starting and defalts """
def _test_init():
    print('minister._test_init - begin')
    minister = Minister(name='Test_Mineister')
    if minister.power_plants != 20 and minister.factories != 20 and minister.mines != 20 and minister.defences != 20 and minister.research != 20:
        print('init fail')
    print('minister._test___init__ - end')
