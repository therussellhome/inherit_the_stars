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
