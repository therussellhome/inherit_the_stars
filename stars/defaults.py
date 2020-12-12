import copy
import traceback
from . import game_engine


""" Class for handling defaults """
class Defaults(game_engine.BaseClass):
    """ Load all defaults into the object """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # populate with initial defaults
        cls = object.__getattribute__(self, '__class__')
        defaults = cls.get_defaults(cls)
        for name in defaults:
            object.__setattr__(self, name, copy.copy(defaults[name][0]))
        # override with provided kwargs
        self.update(**kwargs)

    """ Override the subscript operator """
    def __getitem__(self, name):
        return getattr(self, name)

    """ Override the subscript operator """
    def __setitem__(self, name, value):
        setattr(self, name, value)

    """ Override to enforce type and bounds checking """
    def __setattr__(self, name, value):
        if name[0] != '_':
            cls = object.__getattribute__(self, '__class__')
            defaults = cls.get_defaults(cls)
            if name in defaults:
                default = defaults[name]
                try:
                    if type(default[0]) == int:
                        value = max([default[1], min([default[2], int(value)])])
                    elif type(default[0]) == float:
                        value = max([default[1], min([default[2], float(value)])])
                    elif type(default[0]) == bool:
                        value = bool(value)
                    elif type(default[0]) != type(value):
                        value = copy.copy(default[0])
                except:
                    value = copy.copy(default[0])
        object.__setattr__(self, name, value)

    """ provide a default shallow equality """
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.__dict__.keys() != other.__dict__.keys():
            return False
        for f in self.__dict__.keys():
            if f != '__uuid__' and f != '__cache__' and self.__dict__[f] != other.__dict__[f]:
                return False
        return True

    """ prints the entire __dict__ in a readable way so you can debug if somthing is wrong """
    def debug_display(self, depth=0):
        #TODO REMOVE=(add '#' at the begining of all lines of this function and those pertaining to this function) before release, after finished all tests
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
        for name in kwargs:
            setattr(self, name, kwargs[name])

    """ List of default fields """
    def list_of_defaults(self):
        cls = object.__getattribute__(self, '__class__')
        return cls.get_defaults(cls).keys()

    """ Reset values to default """
    def reset_to_default(self):
        cls = object.__getattribute__(self, '__class__')
        defaults = cls.get_defaults(cls)
        no_reset = getattr(cls, 'no_reset', [])
        for name in defaults:
            if name not in no_reset:
                object.__setattr__(self, name, copy.copy(defaults[name][0]))


""" Store defaults on the class """
def __set_defaults(cls, defaults, sparse_json=True, no_reset=[]):
    cls.defaults = {}
    cls.sparse_json = {}
    for parent in cls.__bases__:
        cls.defaults.update(getattr(parent, 'defaults', {}))
        for (name, value) in getattr(parent, 'sparse_json', {}).items():
            cls.sparse_json[name] = (cls.sparse_json.get(name, sparse_json) and value)
    cls.defaults.update(defaults)
    for name in defaults:
        cls.sparse_json[name] = (cls.sparse_json.get(name, sparse_json) and sparse_json)
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
