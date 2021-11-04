import copy
import uuid
from . import game_engine


""" Class for handling defaults """
class Defaults(game_engine.BaseClass):
    """ Load all defaults into the object """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_defaults(self)
        # override from passed in object
        if len(args) > 0:
            copy_from(self, args[0])
        # override with provided kwargs
        for (k, v) in kwargs.items():
            setattr(self, k, v)
        # create a dictionary that is not written to file
        object.__setattr__(self, '__cache__', {})

    """ Override the subscript operator defaulting to reading from the cache """
    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except:
            return getattr(self, '__cache__')[name]

    """ Override the subscript operator """
    def __setitem__(self, name, value):
        setattr(self, name, value)

    """ Override to enforce type and bounds checking """
    def __setattr__(self, name, value):
        if name[0] != '_':
            default = get_default(self, name)
            if default is not None:
                try:
                    if isinstance(default, bool):
                        value = bool(value)
                    elif isinstance(default, int):
                        value = int(value)
                    elif isinstance(default, float):
                        value = float(value)
                    elif isinstance(value, type(default)):
                        pass
                    else:
                        return
                    default_range = getattr(self.__class__, 'default_ranges', {}).get(name, None)
                    if default_range:
                        value = max(default_range[0], min(default_range[1], value))
                except:
                    return
        object.__setattr__(self, name, value)

    """ provide a default shallow equality """
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.__dict__.keys() != other.__dict__.keys():
            return False
        classname = self.__class__.__name__ + '/'
        for f in self.__dict__.keys():
            if f != '__cache__' and self.__dict__[f] != other.__dict__[f]:
                return False
        return True


""" Store defaults on the class """
def __set_defaults(cls, defaults, sparse_json=True):
    cls.defaults = {}
    cls.default_ranges = {}
    cls.sparse_json = {}
    for parent in cls.__bases__:
        cls.defaults.update(getattr(parent, 'defaults', {}))
        cls.default_ranges.update(getattr(parent, 'default_ranges', {}))
        for (k, v) in getattr(parent, 'sparse_json', {}).items():
            cls.sparse_json[k] = (cls.sparse_json.get(k, sparse_json) and v)
    for (k, default) in defaults.items():
        if isinstance(default, tuple):
            cls.defaults[k] = default[0]
            cls.default_ranges[k] = (default[1], default[2])
        else:
            cls.defaults[k] = default
        cls.sparse_json[k] = (cls.sparse_json.get(k, sparse_json) and sparse_json)
Defaults.set_defaults = __set_defaults


""" Write/overwrite with defaults """
def apply_defaults(obj):
    # populate with initial defaults
    obj_dict = object.__getattribute__(obj, '__dict__')
    for key in getattr(object.__getattribute__(obj, '__class__'), 'defaults', {}).keys():
        obj_dict[key] = get_default(obj, key)


""" Copy attributes from the other object"""
def copy_from(obj, other):
    # copy from other object
    for key in getattr(object.__getattribute__(obj, '__class__'), 'defaults', {}).keys():
        if hasattr(other, key):
            setattr(obj, key, copy.copy(getattr(other, key)))


""" Get the default for a field """
def get_default(obj, field):
    default = getattr(obj.__class__, 'defaults', {}).get(field, None)
    if isinstance(default, str) and default == '@UUID':
        return str(uuid.uuid4())
    return copy.deepcopy(default)
