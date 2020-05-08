import unittest
from .. import *

class GameEngineTestCase(unittest.TestCase):
    def setUp(self):
        self.game_engine = game_engine.GameEngine
    def _test():
        _test_reference()
    _test_load_save()
    _test_unregister()
    _test_defaults()
    
    def _test_reference():
        register(__TestClass)
        t = __TestClass(name='ref 1')
        r = Reference('__TestClass', 'ref 1')
        if r.name != 'ref 1':
        if r.get_name() != 'ref 1':
        t.name = 'ref 2'
        if r.get_name() != 'ref 2':
        r2 = Reference('__TestClass', 'ref 3')
        if r2.get_name() != 'ref 3':
    
    def _test_load_save():
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
    
    def _test_unregister():
        register(__TestClass)
        t = __TestClass(name='unreg 1')
        t.unreg = True
        r = Reference('__TestClass', 'unreg 1')
        unregister(t)
        if r.unreg:
            print('game_engine._test_unregister - ERROR: failed to unregister object')
    
    def _test_defaults():
        register(__TestClass, defaults=__TestClass.defaults)
        t = __TestClass(name='defaults 1')
        if t.defaulted != 12345:
        t.defaulted = 54321
        if t.defaulted != 54321:
        t.defaulted = -1
        if t.defaulted != 0:
    
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
