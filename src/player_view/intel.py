from .. import engine

class Intel():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        classname = object.__getattribute__(self, '__class__').__name__
        if classname in _defaults:
            for name in _defaults[classname]:
                object.__setattr__(self, name, Defaults.__getattribute__(self, name))
        if 'date' not in kwargs:
            self.date = engine.get_game().date

