import unittest
from pathlib import Path
from .. import *


class _TestGameEngine(game_engine.BaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ID = kwargs.get('ID', str(id(self)))
        self.register = kwargs.get('register', True)
        self.abc = kwargs.get('abc', 123)
        self.xyz = {'a': 42}
        self.saved = False
        self.ref = reference.Reference('_TetGameEngine')
        if self.register:
            game_engine.register(self)
    def save(self):
        self.saved = True

class _TestGameEngineErr(game_engine.BaseClass):
    def __init__(self):
        a = b

class GameEngineTestCase(unittest.TestCase):
    def onSetup():
        self.ut_dir = Path.home() / 'Inherit!' / 'test'
        self.ut_dir.unlink(missing_ok=True)

    def test_register_n_get1(self):
        # Nothing in the register
        game_engine.unregister()
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 0)

    def test_register_n_get2(self):
        # Still nothing in the register
        game_engine.unregister()
        t1 = _TestGameEngine(ID='test_get1', register=False)
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 0)

    def test_register_n_get2(self):
        # t1 in the register
        game_engine.unregister()
        t1 = _TestGameEngine(ID='test_get1')
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 1)
        # What is in the register is actually t1
        self.assertEqual(ts[0].ID, t1.ID)
        # Verify reference
        t1.ID = 'test_get1a'
        self.assertEqual(ts[0].ID, t1.ID)

    def test_register_n_get3(self):
        # Add t2
        game_engine.unregister()
        t1 = _TestGameEngine(ID='test_get1')
        t2 = _TestGameEngine(ID='test_get2')
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 2)
        self.assertEqual(ts[0].ID, t1.ID)
        self.assertEqual(ts[1].ID, t2.ID)

    def test_register_n_get4(self):
        # Get a single object
        game_engine.unregister()
        t2 = _TestGameEngine(ID='test_get4')
        t0 = game_engine.get('_TestGameEngine/test_get4')
        self.assertEqual(t0.ID, t2.ID)

    def test_register_n_get5(self):
        # Don't create a new object
        game_engine.unregister()
        t0 = game_engine.get('_TestGameEngine/test_get5')
        self.assertEqual(t0, None)

    def test_register_n_get6(self):
        # Create an object
        game_engine.unregister()
        t0 = game_engine.get('_TestGameEngine/test_get6', True)
        self.assertEqual(t0.ID, 'test_get6')

    def test_register_n_get7(self):
        # Test None
        game_engine.unregister()
        self.assertEqual(game_engine.get(None), None)

    def test_register_n_get8(self):
        # Test random junk
        game_engine.unregister()
        self.assertEqual(game_engine.get(123), [])

    def test_register_n_get9(self):
        # Test random junk
        game_engine.unregister()
        self.assertEqual(game_engine.get(None), None)

    def test_register_n_get10(self):
        game_engine.unregister()
        t1 = _TestGameEngine(ID='test_get8')
        self.assertEqual(game_engine.get('_TestGameEngine/' + t1.ID), t1)

    def test_register_n_get11(self):
        game_engine.unregister()
        t1 = _TestGameEngine(ID='test_get8')
        self.assertEqual(game_engine.get('_TestGameEngine/' + str(id(t1))), t1)

    def test_register_n_get12(self):
        # Create an object
        game_engine.unregister()
        t0 = game_engine.get('Not_A_Real_Class/test_get12', True)
        self.assertEqual(t0, None)

    def test_unregister1(self):
        game_engine.unregister()
        t1 = _TestGameEngine(ID='test_unreg1')
        t2 = _TestGameEngine(ID='test_unreg2')
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 2)
        # Unregister all
        game_engine.unregister()
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 0)

    def test_unregister2(self):
        # Specific object unregister
        game_engine.unregister()
        t1 = _TestGameEngine(ID='test_unreg1')
        t2 = _TestGameEngine(ID='test_unreg2')
        game_engine.unregister(t1)
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 1)
        self.assertEqual(ts[0].ID, t2.ID)
    
    def test_unregister3(self):
        game_engine.unregister()
        t1 = _TestGameEngine(ID='test_unreg3')
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 1)
        game_engine.set_auto_save(t1)
        # Unregister t1
        game_engine.unregister(t1)
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 0)
        game_engine.auto_save()
        self.assertEqual(t1.saved, False)

    def test_autosave1(self):
        game_engine.unregister()
        t1 = _TestGameEngine(ID='test_save1')
        game_engine.set_auto_save(t1)
        self.assertEqual(t1.saved, False)
        game_engine.auto_save()
        self.assertEqual(t1.saved, True)

    def test_json1(self):
        t1 = _TestGameEngine(ID='test_json')
        json = game_engine.to_json(t1)
        t2 = game_engine.from_json(json)
        self.assertEqual(t1.ID, t2.ID)
    
    def test_json2(self):
        self.assertEqual(game_engine.from_json('this is bad json and is supposed to print'), None)
        self.assertEqual(game_engine.to_json({self: ''}), None)

    def test_json3(self):
        t1 = _TestGameEngine(ID='test_json')
        t1.__cache__ = 'abc'
        json = game_engine.to_json(t1)
        t2 = game_engine.from_json(json)
        self.assertFalse(hasattr(t2, '__cache__'))

    def test_load_inspect(self):
        game_engine.unregister()
        t1 = _TestGameEngine(ID='inspect')
        game_engine.save('test', 'inspect', t1)
        game_engine.unregister()
        t2 = game_engine.load_inspect('test', 'inspect')
        self.assertEqual(t2.ID, 'inspect')
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 0)

    def test_save_load1(self):
        game_engine.unregister()
        t1 = _TestGameEngine(ID='save_load')
        t1.l = [1,2,3]
        game_engine.save('test', 'save_load', t1)
        game_engine.unregister()
        t2 = game_engine.load('test', 'save_load')
        self.assertEqual(t2.ID, 'save_load')
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 1)
        self.assertEqual(ts[0].ID, 'save_load')

    def test_save_load2(self):
        game_engine.unregister()
        t1 = _TestGameEngine(ID='sparse', abc=555)
        t1.__class__.defaults = {'abc': 555, 'saved': True}
        t1.__class__.sparse_json = {'abc': True, 'saved': True, 'xyz': False}
        game_engine.save('test', 'sparse', t1)
        game_engine.unregister()
        t2 = game_engine.load('test', 'sparse')
        self.assertEqual(t2.ID, 'sparse')
        ts = game_engine.get('_TestGameEngine')
        self.assertEqual(len(ts), 1)
        self.assertEqual(ts[0].ID, 'sparse')
        self.assertEqual(ts[0].abc, 123)

    def test_list(self):
        game_engine.unregister()
        t = _TestGameEngine(ID='list')
        game_engine.save('test', '_list', t)
        game_engine.unregister()
        # Testing list has to be done after save
        l = game_engine.load_list('test')
        self.assertGreater(len(l), 1)

    def test_load1(self):
        game_engine.unregister()
        # Testing list has to be done after save
        t = game_engine.load('test', '_list0')
        self.assertEqual(t.ID, 'list0')

    def test_load2(self):
        game_engine.unregister()
        # Testing list has to be done after save
        t = game_engine.load('test', '_load')
        self.assertEqual(len(t), 2)

    def test_load3(self):
        game_engine.unregister()
        # Testing list has to be done after save
        t = game_engine.load('test', '_empty')
        self.assertEqual(len(t), 0)

    def test_new1(self):
        with self.assertRaises(Exception):
            game_engine.get('_TestGameEngineErr/1', True)

