import os
import unittest
from .. import *

""" Test class for unit testing """
class _TestClass(game_engine.Defaults):
    defaults = {'defaulted': [12345, 0, 99999]}
    def __init__(self, **kwargs):
        self.name = 'unnamed'
        self.unreg = False
        for k in kwargs:
            self.__dict__[k] = kwargs[k]
        game_engine.register(self)
    
    def get_name(self):
        return self.name
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == 'name':
            game_engine.register(self)

class GameEngineTestCase(unittest.TestCase):
    def onSetup():
        game_engine.register(_TestClass)
        os.remove('games/unittest.zip')

    def test_reference(self):
        t = _TestClass(name='ref 1')
        r = game_engine.Reference('_TestClass', 'ref 1')
        self.assertEqual(r.name, 'ref 1')
        self.assertEqual(r.get_name(), 'ref 1')
        t.name = 'ref 2'
        self.assertEqual(r.get_name(), 'ref 2')
        r2 = game_engine.Reference('_TestClass', 'ref 3')
        self.assertEqual(r2.get_name(), 'ref 3')
    
    def test_load_save(self):
        t = _TestClass(name='load 1')
        game_engine.save_game('games/unittest.zip')
        t.name = 'load 2'
        game_engine.load_game('games/unittest.zip')
        r = game_engine.Reference('_TestClass', 'load 1')
        self.assertEqual(r.name, 'load 1')
    
    def test_unregister(self):
        t = _TestClass(name='unreg 1')
        t.unreg = True
        r = game_engine.Reference('_TestClass', 'unreg 1')
        game_engine.unregister(t)
        self.assertFalse(r.unreg)
    
    def test_defaults(self):
        game_engine.register(_TestClass, defaults=_TestClass.defaults)
        t = _TestClass(name='defaults 1')
        self.assertEqual(t.defaulted, 12345)
        t.defaulted = 54321
        self.assertEqual(t.defaulted, 54321)
        t.defaulted = -1
        self.assertEqual(t.defaulted, 0)
