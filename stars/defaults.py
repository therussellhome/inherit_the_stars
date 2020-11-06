import copy
from . import game_engine


""" Class for handling defaults """
class Defaults(game_engine.BaseClass):
    """ Load all defaults into the object """
    def __init__(self, **kwargs):
        self.update(**kwargs)
        cls = object.__getattribute__(self, '__class__')
        defaults = cls.get_defaults(cls)
        for name in defaults:
            object.__setattr__(self, name, Defaults.__getattribute__(self, name))

    """ Override to enforce type and bounds checking """
    def __getattribute__(self, name):
        if name[0] == '_' :
            return object.__getattribute__(self, name)
        cls = object.__getattribute__(self, '__class__')
        defaults = cls.get_defaults(cls)
        if name in defaults:
            default = defaults[name]
            try:
                value = object.__getattribute__(self, name)
                if type(default[0]) == int:
                    return max([default[1], min([default[2], int(value)])])
                elif type(default[0]) == float:
                    return max([default[1], min([default[2], float(value)])])
                elif type(default[0]) == bool:
                    return bool(value)
                elif type(default[0]) == type(value):
                    return value
            except:
                pass
            return copy.copy(default[0])
        return object.__getattribute__(self, name)
    
    """ prints the entire __dict in a readable way so you can debug if somthing is wrong """
    def debug_display(self, depth=0):
        print('{', 'class: ', self.__class__, sep='')
        for attribute in self.__dict__:
            try:
                print('    '*(depth+1), str(attribute), ": ", sep='', end='')
                self.__dict__[attribute].debug_display(depth+1)
            except:
                print(getattr(self, attribute))
        print('    '*depth, '}', sep='')

    """ Bulk update values """
    def update(self, **kwargs):
        cls = object.__getattribute__(self, '__class__')
        defaults = cls.get_defaults(cls)
        for name in kwargs:
            value = kwargs[name]
            if name in defaults:
                default = defaults[name]
                try:
                    if type(default[0]) == int:
                        value = max([default[1], min([default[2], int(value)])])
                    elif type(default[0]) == float:
                        value = max([default[1], min([default[2], float(value)])])
                    elif type(default[0]) == bool:
                        value = bool(value)
                    elif type(default[0]) == type(value):
                        pass
                except:
                    value = copy.copy(default[0])
            object.__setattr__(self, name, value)

    """ Reset values to default """
    def reset_to_default(self):
        cls = object.__getattribute__(self, '__class__')
        defaults = cls.get_defaults(cls)
        no_reset = getattr(cls, 'no_reset', [])
        for name in defaults:
            if name not in no_reset:
                object.__setattr__(self, name, copy.copy(defaults[name][0]))


""" Store defaults on the class """
def __set_defaults(cls, defaults, no_reset=[]):
    cls.defaults = {}
    for parent in cls.__bases__:
        cls.defaults.update(getattr(parent, 'defaults', {}))
    cls.defaults.update(defaults)
    cls.no_reset = no_reset
    for parent in cls.__bases__:
        cls.no_reset.extend(getattr(parent, 'no_reset', []))
Defaults.set_defaults = __set_defaults


""" Get defaults from the class """
def __get_defaults(cls):
    if not hasattr(cls, 'defaults'):
        cls.set_defaults(cls, {})
    return cls.defaults
Defaults.get_defaults = __get_defaults
