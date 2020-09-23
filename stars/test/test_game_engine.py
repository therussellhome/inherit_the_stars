import unittest
from pathlib import Path
from .. import *


class _TestGameEngine(game_engine.BaseClass):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', str(id(self)))
        self.dict = {'abc': 'xzy'}


class GameEngineTestCase(unittest.TestCase):
    def onSetup():
        self.ut_file = Path.home() / 'Inherit!' / 'test' / 'unittest.zip'
        self.ut_file.unlink(missing_ok=True)

    def test_register_n_get(self):
        # Nothing in the register
        game_engine.unregister()
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 0)
        # Still nothing in the register
        t1 = _TestGameEngine(name='test_get1')
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 0)
        # t1 in the register
        game_engine.register(t1)
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 1)
        # What is in the register is actually t1
        self.assertEqual(ts[0].name, t1.name)
        # Verify reference
        t1.name = 'test_get1a'
        self.assertEqual(ts[0].name, t1.name)
        # Add t2
        t2 = _TestGameEngine(name='test_get2')
        game_engine.register(t2)
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 2)
        self.assertEqual(ts[0].name, t1.name)
        self.assertEqual(ts[1].name, t2.name)
        # Get a single object
        t0 = game_engine.get('_TestGameEngine/test_get2')
        self.assertEqual(t0.name, t2.name)
        # Don't create a new object
        t0 = game_engine.get('_TestGameEngine/test_get0')
        self.assertEqual(t0, None)
        # Create an object
        t0 = game_engine.get('_TestGameEngine/test_get0', True)
        self.assertEqual(t0.name, 'test_get0')
        # Test errors
        with self.assertRaises(LookupError):
            game_engine.get(0)

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

    def test_load_save_list(self):
        game_engine.unregister()
        t = _TestGameEngine(name='test_save')
        game_engine.register(t)
        game_engine.save('test', 'unittest')
        game_engine.unregister()
        # Names have been changed to protect the guilty
        t.name = 'test_load'
        # Load without registering
        ts = game_engine.load('test', 'unittest', False)
        self.assertNotEqual(ts[0].name, t.name)
        self.assertEqual(ts[0].name, 'test_save')
        # Load and inspect
        tl = game_engine.load_inspect('test', 'unittest', '_TestGameEngine')
        self.assertEqual(len(tl), 1)
        self.assertEqual(tl[0], 'test_save')
        # Load and register
        game_engine.load('test', 'unittest')
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 1)
        self.assertEqual(ts[0].name, 'test_save')
        # Testing list has to be done after save
        l = game_engine.load_list('test')
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0], 'unittest')

    def test_load_defaults(self):
        game_engine.unregister()
        ts = game_engine.load_defaults('Tech')
        self.assertGreater(len(ts), 0)
        self.assertEqual(ts[0].__class__.__name__, 'Tech')
        ts = game_engine.get('Tech')
        self.assertEqual(len(ts), 0)
        ts = game_engine.load_defaults('Tech', True)
        ts = game_engine.get('Tech')
        self.assertGreater(len(ts), 0)
