import json
import os
import shutil
from zipfile import ZipFile, ZipInfo
from serializable import Serializable

""" Private registry of all game objects """
__registry = {}

""" Receive registration of the objects as they self-register """
""" allow for re-registration """
def register(type_name, obj):
    for key, value in __registry.items():
        if value == obj:
            del __registry[key]
            break
    __registry[type_name] = obj

""" Return a registered object """
def get(type_name):
    if type_name in __registry:
        return __registry[type_name]
    return None

""" Load game from zip file """
def load_game(path):
    with ZipFile(path, 'r') as zipfile:
        for info in zipfile.infolist():
            register(info.filename, json.loads(zipfile.read(info), object_hook=__decode))

""" Save game to zip file """
def save_game(path):
    with ZipFile(path, 'w') as zipfile:
        for type_name in __registry:
            zipfile.writestr(ZipInfo(type_name), json.dumps(__registry[type_name], default=__encode))

""" Custom encoder to handle classes """
def __encode(obj):
    values = obj.__dict__
    values['__class__'] = obj.__class__.__name__
    return values

""" Custom decoder to handle classes """
def __decode(values):
    if '__class__' in values:
        for subclass in Serializable.__subclasses__():
            if subclass.__name__ == values['__class__']:
                obj = subclass()
                obj.__dict__ = values
                return obj
    return values


""" Test method """
def _test():
    print('game_engine._test - begin')
    _test_load_save()
    print('game_engine._test - end')

""" Test method """
def _test_load_save():
    print('game_engine._test_load_save - begin')
    try:
        shutil.rmtree('test_output/')
    except:
        pass
    os.makedirs('test_output/', exist_ok=True)
    t = __TestClass()
    t1 = get('test/game_engine')
    if t1.name != 'test 1':
        print('game_engine._test - ERROR: get() did not return the correct object')
    t.name = 'test 2'
    if t1.name != 'test 2':
        print('game_engine._test - ERROR: modification to original object not found in object from get()')
    save_game('test_output/game_engine_test.zip')
    t.name = 'test 3'
    load_game('test_output/game_engine_test.zip')
    t2 = get('test/game_engine')
    if t2.name != 'test 2':
        print('game_engine._test - ERROR: save_game/load_game did not preserve object')
    #shutil.rmtree('test_output/')
    print('game_engine._test_load_save - end')

""" Class used for testing """
class __TestClass(Serializable):
    def __init__(self):
        self.name = 'test 1'
        register('test/game_engine', self)
