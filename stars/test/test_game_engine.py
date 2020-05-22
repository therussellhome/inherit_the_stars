import unittest
from pathlib import Path
from .. import *


class _TestGameEngine(game_engine.BaseClass):
    def __init__(self, **kwargs):
        self.unreg = False
        self.name = kwargs.get('name', str(id(self)))
        game_engine.register(self)


class GameEngineTestCase(unittest.TestCase):
    def onSetup():
        p = Path.home() / 'stars' / 'inherit' / 'test' / 'unittest.zip'
        p.unlink(missing_ok=True)

    def test_load_save(self):
        t = _TestGameEngine(name='load 1')
        game_engine.save('test', 'unittest')
        t.name = 'load 2'
        game_engine.load('test', 'unittest')
        r = reference.Reference('_TestGameEngine', 'load 1')
        self.assertEqual(r.name, 'load 1')
    
    def test_unregister(self):
        t = _TestGameEngine(name='unreg 1')
        t.unreg = True
        r = reference.Reference('_TestGameEngine', 'unreg 1')
        game_engine.unregister(t)
        self.assertFalse(r.unreg)
