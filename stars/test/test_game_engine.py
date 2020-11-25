import unittest
from pathlib import Path
from .. import *


class _TestGameEngine(game_engine.BaseClass):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', str(id(self)))
        self.dict = {'abc': 'xzy'}


class GameEngineTestCase(unittest.TestCase):
    def onSetup():
        self.ut_file = Path.home() / 'Inherit!' / 'test' / 'unittest'
        self.ut_file.unlink(missing_ok=True)

    def test_register_n_get1(self):
        # Nothing in the register
        game_engine.unregister()
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 0)

    def test_register_n_get2(self):
        # Still nothing in the register
        game_engine.unregister()
        t1 = _TestGameEngine(name='test_get1')
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 0)

    def test_register_n_get2(self):
        # t1 in the register
        game_engine.unregister()
        t1 = _TestGameEngine(name='test_get1')
        game_engine.register(t1)
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 1)
        # What is in the register is actually t1
        self.assertEqual(ts[0].name, t1.name)
        # Verify reference
        t1.name = 'test_get1a'
        self.assertEqual(ts[0].name, t1.name)

    def test_register_n_get3(self):
        # Add t2
        game_engine.unregister()
        t1 = _TestGameEngine(name='test_get1')
        game_engine.register(t1)
        t2 = _TestGameEngine(name='test_get2')
        game_engine.register(t2)
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 2)
        self.assertEqual(ts[0].name, t1.name)
        self.assertEqual(ts[1].name, t2.name)

    def test_register_n_get4(self):
        # Get a single object
        game_engine.unregister()
        t2 = _TestGameEngine(name='test_get2')
        game_engine.register(t2)
        t0 = game_engine.get('_TestGameEngine', 'test_get2')
        self.assertEqual(t0.name, t2.name)

    def test_register_n_get5(self):
        # Don't create a new object
        game_engine.unregister()
        t0 = game_engine.get('_TestGameEngine', 'test_get0')
        self.assertEqual(t0, None)

    def test_register_n_get6(self):
        # Create an object
        game_engine.unregister()
        t0 = game_engine.get('_TestGameEngine', 'test_get0', True)
        self.assertEqual(t0.name, 'test_get0')

    def test_register_n_get6(self):
        # Test None
        game_engine.unregister()
        self.assertEqual(game_engine.get(None), None)

    def test_register_n_get6(self):
        # Test random junk
        game_engine.unregister()
        self.assertEqual(game_engine.get(123), [])

    def test_unregister(self):
        game_engine.unregister()
        t1 = _TestGameEngine(name='test_unreg1')
        game_engine.register(t1)
        t2 = _TestGameEngine(name='test_unreg2')
        game_engine.register(t2)
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 2)
        # Specific object unregister
        game_engine.unregister(t1)
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 1)
        self.assertEqual(ts[0].name, t2.name)
        # Unregister all
        game_engine.register(t1)
        game_engine.unregister()
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 0)
    
    def test_json(self):
        t1 = _TestGameEngine(name='test_json')
        json = game_engine.to_json(t1)
        t2 = game_engine.from_json(json)
        self.assertEqual(t1.name, t2.name)
        self.assertEqual(game_engine.from_json('this is bad json and is supposed to print'), None)

    def test_load_save_list(self):
        game_engine.unregister()
        t = _TestGameEngine(name='test_save')
        game_engine.register(t)
        game_engine.save('test', 'unittest', t)
        game_engine.unregister()
        # Names have been changed to protect the guilty
        t.name = 'test_load'
        # Load
        ts = game_engine.load('test', 'unittest')
        self.assertNotEqual(ts.name, t.name)
        self.assertEqual(ts.name, 'test_save')
        # Testing list has to be done after save
        l = game_engine.load_list('test')
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0], 'unittest')

    def test_load_defaults(self):
        game_engine.unregister()
        ts = game_engine.load_defaults('Tech')
        self.assertGreater(len(ts), 0)
        self.assertEqual(ts[0].__class__.__name__, 'Tech')
