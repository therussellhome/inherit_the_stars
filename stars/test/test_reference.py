import unittest
from .. import *

class _TestReference(game_engine.BaseClass):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', str(id(self)))
        game_engine.register(self)

    def get_name(self):
        return self.name

class ReferenceTestCase(unittest.TestCase):
    def test_access(self):
        t = _TestReference(name='ref 1')
        r = reference.Reference('_TestReference', 'ref 1')
        self.assertEqual(r.name, 'ref 1')
        self.assertEqual(r.get_name(), 'ref 1')

    def test_create(self):
        r = reference.Reference('_TestReference', 'ref 2')
        self.assertEqual(r.name, 'ref 2')

    def test_throw(self):
        r = reference.Reference('_TestRef', 'ref 3')
        with self.assertRaises(LookupError):
            r.get_name()
