import json
import os
import shutil
import inspect
from zipfile import ZipFile, ZipInfo

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
                return default[0]
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
                return (obj == None)
            elif obj != None:
                return obj.__getattribute__(name)
            else:
                raise AttributeError('"' + str(reference) + '" is not registered')

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
                raise AttributeError('"' + str(reference) + '" is not registered')

# Register the class with the game engine
register(Reference)


""" Load game from zip file """
def load_game(path):
    with ZipFile(path, 'r') as zipfile:
        for info in zipfile.infolist():
            register(json.loads(zipfile.read(info), object_hook=__decode))

""" Save game to zip file """
def save_game(path):
    with ZipFile(path, 'w') as zipfile:
        for name in _registry:
            zipfile.writestr(ZipInfo(name), json.dumps(_registry[name], default=__encode))


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


""" Test method """
def _test():
    print('game_engine._test - begin')
    _test_reference()
    _test_load_save()
    _test_unregister()
    _test_defaults()
    print('game_engine._test - end')

""" Test the reference class """
def _test_reference():
    print('game_engine._test_reference - begin')
    register(__TestClass)
    t = __TestClass(name='ref 1')
    r = Reference('__TestClass', 'ref 1')
    if r.name != 'ref 1':
        print('game_engine._test_reference - ERROR: attribute access does not work')
    if r.get_name() != 'ref 1':
        print('game_engine._test_reference - ERROR: method access does not work')
    t.name = 'ref 2'
    if r.get_name() != 'ref 2':
        print('game_engine._test_reference - ERROR: reference did not refer back to original object')
    r2 = Reference('__TestClass', 'ref 3')
    if r2.get_name() != 'ref 3':
        print('game_engine._test_reference - ERROR: reference did not properly create a new object')
    print('game_engine._test_reference - end')

""" Test load and save """
def _test_load_save():
    print('game_engine._test_load_save - begin')
    register(__TestClass)
    try:
        shutil.rmtree('test_output/')
    except:
        pass
    os.makedirs('test_output/', exist_ok=True)
    t = __TestClass(name='load 1')
    save_game('test_output/game_engine_test.zip')
    t.name = 'load 2'
    load_game('test_output/game_engine_test.zip')
    r = Reference('__TestClass', 'load 1')
    if r.name == None:
        print('game_engine._test_load_save - ERROR: save_game/load_game did not preserve object')
    #shutil.rmtree('test_output/')
    print('game_engine._test_load_save - end')

""" Test unregister """
def _test_unregister():
    print('game_engine._test_unregister - begin')
    register(__TestClass)
    t = __TestClass(name='unreg 1')
    t.unreg = True
    r = Reference('__TestClass', 'unreg 1')
    unregister(t)
    if r.unreg:
        print('game_engine._test_unregister - ERROR: failed to unregister object')
    print('game_engine._test_unregister - end')

""" Test unregister """
def _test_defaults():
    print('game_engine._test_defaults - begin')
    register(__TestClass, defaults=__TestClass.defaults)
    t = __TestClass(name='defaults 1')
    if t.defaulted != 12345:
        print('game_engine._test_defaults - ERROR: failed to get defaults value')
    t.defaulted = 54321
    if t.defaulted != 54321:
        print('game_engine._test_defaults - ERROR: failed to set value')
    t.defaulted = -1
    if t.defaulted != 0:
        print('game_engine._test_defaults - ERROR: failed to enforce range')
    print('game_engine._test_defaults - end')

""" Class used for testing """
class __TestClass(Defaults):
    defaults = {'defaulted': [12345, 0, 99999]}

    def __init__(self, **kwargs):
        self.name = 'unnamed'
        self.unreg = False
        for k in kwargs:
            self.__dict__[k] = kwargs[k]
        register(self)
    def get_name(self):
        return self.name
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == 'name':
            register(self)
