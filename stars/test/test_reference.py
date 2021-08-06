import unittest
from .. import *

class _TestReference(game_engine.BaseClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ID = kwargs.get('ID', str(id(self)))
        self.abc = 0
        game_engine.register(self)

    def get_id(self):
        return self.ID

class ReferenceTestCase(unittest.TestCase):
    def test_access(self):
        game_engine.unregister()
        t = _TestReference(ID='access')
        r = reference.Reference('_TestReference', 'access')
        self.assertEqual(r.ID, 'access')
        self.assertEqual(r.get_id(), 'access')

    def test_create1(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference/create')
        self.assertEqual(r.ID, 'create')

    def test_create2(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference', 'create')
        self.assertEqual(r.ID, 'create')

    def test_create3(self):
        game_engine.unregister()
        r = reference.Reference(__reference__='_TestReference/create')
        self.assertEqual(r.ID, 'create')

    def test_create4(self):
        game_engine.unregister()
        with self.assertRaises(LookupError):
            r = reference.Reference(5)

    def test_create5(self):
        game_engine.unregister()
        r1 = reference.Reference('_TestReference/create')
        r2 = reference.Reference(r1)
        self.assertEqual(r2.ID, 'create')

    def test_create6(self):
        game_engine.unregister()
        t = _TestReference(ID='create')
        r = reference.Reference(t)
        self.assertEqual(r.ID, 'create')

    def test_get2(self):
        game_engine.unregister()
        r = reference.Reference()
        with self.assertRaises(LookupError):
            r.get_id()

    def test_get3(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference/get')
        self.assertEqual(r.ID, 'get')

    def test_get4(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference')
        self.assertNotEqual(r.get_id(), '')

    def test_get5(self):
        game_engine.unregister()
        r = reference.Reference('int/')
        with self.assertRaises(LookupError):
            r.get_id()
    
    def test_get6(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference/get')
        self.assertEqual(r['abc'], 0)

    def test_invert1(self):
        game_engine.unregister()
        t = _TestReference(ID='invert')
        r = reference.Reference(t)
        self.assertEqual(~r, t)

    def test_set1(self):
        game_engine.unregister()
        r = reference.Reference()
        with self.assertRaises(LookupError):
            r.abc = 123

    def test_set2(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference')
        r.ID = 'set'
        self.assertEqual(r.ID, 'set')

    def test_set3(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference')
        r.abc = 123
        self.assertEqual(r.abc, 123)

    def test_set4(self):
        game_engine.unregister()
        r = reference.Reference('_TestReference')
        r.ID = 'set'
        self.assertEqual(r.get_id(), 'set')

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

    def test_eq4(self):
        t1 = _TestReference()
        r1 = reference.Reference(t1)
        self.assertTrue(r1 == t1)

    def test_valid1(self):
        r1 = reference.Reference('_TestReference/bool')
        self.assertFalse(r1)

    def test_valid2(self):
        r1 = reference.Reference('_TestReference/bool')
        r1['abc'] = 6
        self.assertTrue(r1)

    def test_valid3(self):
        r1 = reference.Reference()
        self.assertFalse(r1)

    def test_xor1(self):
        r1 = reference.Reference('_TestReference/xor')
        self.assertTrue(r1 ^ '_TestReference')

    def test_map1(self):
        r1 = reference.Reference('_TestReference/map')
        m = {r1: 'abc'}
        self.assertEqual(m[r1], 'abc')
