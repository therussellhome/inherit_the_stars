import unittest
from .. import *

class _TestReference(game_engine.BaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name', str(id(self)))
        self.abc = 0
        game_engine.register(self)

    def get_name(self):
        return self.name

class ReferenceTestCase(unittest.TestCase):
    def test_access(self):
        game_engine.unregister()
        t = _TestReference(name='access')
        r = reference.Reference('_TestReference', 'access')
        self.assertEqual(r.name, 'access')
        self.assertEqual(r.get_name(), 'access')

    def test_create1(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference/create')
        self.assertEqual(r.name, 'create')

    def test_create2(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference', 'create')
        self.assertEqual(r.name, 'create')

    def test_create3(self):
        game_engine.unregister()
        r = reference.Reference(_reference='_TestReference/create')
        self.assertEqual(r.name, 'create')

    def test_create4(self):
        game_engine.unregister()
        with self.assertRaises(LookupError):
            r = reference.Reference(5)

    def test_create5(self):
        game_engine.unregister()
        r1 = reference.Reference('_TestReference/create')
        r2 = reference.Reference(r1)
        self.assertEqual(r2.name, 'create')

    def test_create6(self):
        game_engine.unregister()
        t = _TestReference(name='create')
        r = reference.Reference(t)
        print(t.__uuid__, r._reference)
        self.assertEqual(r.name, 'create')

    def test_get1(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference/')
        self.assertFalse(r.is_valid)

    def test_get2(self):
        game_engine.unregister()
        r = reference.Reference()
        with self.assertRaises(LookupError):
            r.get_name()

    def test_get3(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference/get')
        self.assertEqual(r.name, 'get')

    def test_get4(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference')
        self.assertNotEqual(r.get_name(), '')

    def test_get5(self):
        game_engine.unregister()
        r = reference.Reference('int/')
        with self.assertRaises(LookupError):
            r.get_name()
    
    def test_get6(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference/get')
        self.assertEqual(r['abc'], 0)

    def test_set1(self):
        game_engine.unregister()
        r = reference.Reference()
        with self.assertRaises(LookupError):
            r.abc = 123

    def test_set2(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference')
        r.name = 'set'
        self.assertEqual(r.name, 'set')

    def test_set3(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference')
        r.abc = 123
        self.assertEqual(r.abc, 123)

    def test_set4(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference')
        r.name = 'set'
        self.assertEqual(r.get_name(), 'set')

    def test_set5(self):
        game_engine.unregister()
        r = reference.Reference('int/')
        with self.assertRaises(LookupError):
            r.abc = 123

    def test_set6(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference/set')
        r['abc'] = 6
        self.assertEqual(r.abc, 6)

    def test_eq1(self):
        r1 = reference.Reference('_TestReference/eq')
        self.assertFalse(r1 == None)

    def test_eq2(self):
        r1 = reference.Reference('_TestReference/eq')
        r2 = reference.Reference('_TestReference/eq')
        self.assertTrue(r1 == r2)

    def test_eq3(self):
        r1 = reference.Reference('_TestReference/eq')
        r2 = reference.Reference('_TestReference/ne')
        self.assertFalse(r1 == r2)
