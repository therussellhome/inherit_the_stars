import copy
import json
import shutil
import inspect
from pathlib import Path
from zipfile import ZipFile, ZipInfo

""" Directory for save games """
game_dir = Path.home() / 'inherit the stars' / 'games'

""" Directory from race files """
race_dir = Path.home() / 'inherit the stars' / 'races'

""" Private registry of all creatable classes """
_classes = {}

""" Private registry of default values for classes """
_defaults = {}

""" Private registry of all game objects """
""" indexed by classname/registered_name """
_registry = {}

""" List of references for update on reregister """
_references = []

""" Receive registration of classes and objects as they self-register """
""" allow for re-registration """
def register(obj, **kwargs):
    if inspect.isclass(obj):
        _classes[obj.__name__] = obj
        _defaults[obj.__name__] = __merge_defaults(obj)
        if 'defaults' in kwargs:
            _defaults[obj.__name__].update(kwargs['defaults'])
    else:
        if hasattr(obj, 'name'):
            name = obj.__class__.__name__ + '/' + obj.name
            for key, value in _registry.items():
                if value == obj:
                    del _registry[key]
                    for reference in _references:
                        if reference.reference == key:
                            reference.reference = name
                    break
            _registry[name] = obj

""" Unregister objects to keep them from being part of the save game """
def unregister(obj):
    for key, value in _registry.items():
        if value == obj:
            del _registry[key]
            break

""" Get list of all registered X """
def get_registered(classname):
    objs = []
    classname = classname + '/'
    for key, value in _registry.items():
        if key.startswith(classname):
            objs.append(value)
    return objs

""" Recursively merge class defaults """
def __merge_defaults(cls):
    defaults = {}
    for parent in cls.__bases__:
        defaults.update(__merge_defaults(parent))
    if cls.__name__ in _defaults:
        defaults.update(_defaults[cls.__name__])
    return defaults

""" Base class for handling defaults """
""" Only overriding the get is sufficient to keep safe """
class Defaults:
    """ Override to enforce type and bounds checking """
    def __getattribute__(self, name):
        if name[0] == '_' :
            return object.__getattribute__(self, name)
        classname = object.__getattribute__(self, '__class__').__name__
        if classname in _defaults:
            if name in _defaults[classname]:
                default = _defaults[classname][name]
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

    """ Load all defaults into the object """
    def _apply_defaults(self, **kwargs):
        object.__getattribute__(self, '__dict__').update(kwargs)
        classname = object.__getattribute__(self, '__class__').__name__
        if classname in _defaults:
            for name in _defaults[classname]:
                object.__setattr__(self, name, Defaults.__getattribute__(self, name))


""" Encapsulate a reference to another class that uses the game_engine to lookup """
""" Capable of creating the reference if not already created """
class Reference:
    """ The only supported variable is the reference string """
    def __init__(self, *args, **kwargs):
        global _references
        if 'reference' in kwargs:
            self.reference = kwargs['reference']
        elif len(args) > 1:
            self.reference = args[0] + '/' + args[1]
        elif len(args) == 1:
            self.reference = args[0].__class__.__name__ + '/' + args[0].name
        else:
            self.reference = None
        _references.append(self)

    """ Get the referenced object or None """
    def __get_referenced_object(self):
        reference = object.__getattribute__(self, 'reference')
        if reference == None:
            return None
        (classname, ref_name) = reference.split('/')
        if reference in _registry:
            return _registry[reference]
        elif classname in _classes:
            return _classes[classname](name=ref_name)
        else:
            return None

    """ Get the attribute from the real class """
    def __getattribute__(self, name):
        global _registry, _classes
        if name == 'reference' or name[0] == '_':
            return object.__getattribute__(self, name)
        else:
            obj = self.__get_referenced_object()
            if name == 'is_valid':
                return (obj != None)
            elif obj != None:
                return obj.__getattribute__(name)
            else:
                raise AttributeError('"' + str(object.__getattribute__(self, 'reference')) + '" is not registered')

    """ Set the attribute in the encapsulated class """
    def __setattr__(self, name, value):
        global _registry, _classes
        if name == 'reference' or name[0] == '_':
            self.__dict__[name] = value
        else:
            obj = self.__get_referenced_object()
            if obj != None:
                obj.__setattr__(name, value)
            else:
                raise AttributeError('"' + str(object.__getattribute__(self, 'reference')) + '" is not registered')

# Register the class with the game engine
register(Reference)


""" Decode an object """
def from_json(obj):
	return json.loads(obj, object_hook=__decode)


""" Encode an object """
def to_json(obj):
	return json.dumps(obj, default=__encode)


""" Load game from zip file """
def load_game(game_name):
    game_file = game_dir / (game_name + '.zip')
    with ZipFile(game_file, 'r') as zipfile:
        for info in zipfile.infolist():
            register(from_json(zipfile.read(info)))

""" Save game to zip file """
def save_game(game_name):
    game_file = game_dir / (game_name + '.zip')
    game_file.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(game_file, 'w') as zipfile:
        for name in _registry:
            zipfile.writestr(ZipInfo(name), to_json(_registry[name]))


""" Custom encoder to handle classes """
def __encode(obj):
    values = obj.__dict__.copy()
    values['__class__'] = obj.__class__.__name__
    return values

""" Custom decoder to handle classes """
def __decode(values):
    if '__class__' in values:
        classname = values['__class__']
        if classname in _classes:
            del values['__class__']
            return _classes[classname](**values)
    return values
