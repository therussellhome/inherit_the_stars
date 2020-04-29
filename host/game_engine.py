import json
import os
import shutil
from zipfile import ZipFile, ZipInfo

""" Private registry of all creatable classes """
_classes = {}

""" Private registry of all game objects """
""" indexed by classname/registered_name """
_registry = {}

""" List of references for update on reregister """
_references = []

""" Receive registration of the classes as they are registered """
def register_class(cls):
    _classes[cls.__name__] = cls

""" Receive registration of the objects as they self-register """
""" allow for re-registration """
def register(obj):
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

""" Encapsulate a reference to another class that uses the game_engine to lookup """
""" Capable of creating the reference if not already created """
class Reference():
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

    """ Get the attribute from the real class """
    def __getattribute__(self, name):
        global _registry, _classes
        if name == 'reference' or name[0] == '_':
            return object.__getattribute__(self, name)
        else:
            classname = None
            reference = object.__getattribute__(self, 'reference')
            if reference != None:
                (classname, ref_name) = reference.split('/')
            if reference in _registry:
                return _registry[reference].__getattribute__(name)
            elif classname in _classes:
                obj = _classes[classname](name=ref_name)
                return obj.__getattribute__(name)
            else:
                raise AttributeError('"' + str(reference) + '" is not registered')

    """ Set the attribute in the encapsulated class """
    def __setattr__(self, name, value):
        global _registry, _classes
        if name == 'reference' or name[0] == '_':
            self.__dict__[name] = value
        else:
            classname = None
            reference = object.__getattribute__(self, 'reference')
            if reference != None:
                (classname, ref_name) = reference.split('/')
            if reference in _registry:
                _registry[reference].__setattr__(name, value)
            elif classname in _classes:
                obj = _classes[classname](name=ref_name)
                obj.__setattr__(name, value)
            else:
                raise AttributeError('"' + str(reference) + '" is not registered')

# Register the class with the game engine
register_class(Reference)


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
    values = obj.__dict__
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
    print('game_engine._test - end')

""" Test the reference class """
def _test_reference():
    print('game_engine._test_reference - begin')
    register_class(__TestClass)
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
    register_class(__TestClass)
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
    register_class(__TestClass)
    t = __TestClass(name='unreg 1')
    t.unreg = True
    r = Reference('__TestClass', 'unreg 1')
    unregister(t)
    if r.unreg:
        print('game_engine._test_unregister - ERROR: failed to unregister object')
    #shutil.rmtree('test_output/')
    print('game_engine._test_unregister - end')

""" Class used for testing """
class __TestClass():
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
