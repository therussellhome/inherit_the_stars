import unittest
from .. import *

_defaults = {
    'default_int': (123, 0, 999),
    'default_float': (0.5, 0.1, 0.9),
    'default_bool': True,
    'default_string': 'string',
    'default_object': ['list'],
    'default_int2': (987, 0, 999),
}

_tmp = {
    'tmp_int': 50,
}

class _TestDefaults(defaults.Defaults):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
_TestDefaults.set_defaults(_TestDefaults, _defaults, _tmp)

class _TestDefaultsChild(_TestDefaults):
    pass

class DefaultsTestCase(unittest.TestCase):
    def test_set_defaults(self):
        self.assertEqual(_TestDefaults.defaults['default_int'], _defaults['default_int'][0])
        self.assertEqual(_TestDefaults.defaults['default_string'], _defaults['default_string'])

    def test_child(self):
        t = _TestDefaultsChild()
        self.assertEqual(t.default_int, 123)
        self.assertEqual(t.default_float, 0.5)
        self.assertEqual(t.default_bool, True)
        self.assertEqual(t.default_string, 'string')
        self.assertEqual(t.default_object[0], 'list')

    def test_no_value(self):
        t = _TestDefaults()
        self.assertEqual(t.default_int, 123)
        self.assertEqual(t.default_float, 0.5)
        self.assertEqual(t.default_bool, True)
        self.assertEqual(t.default_string, 'string')

    def test_kwargs(self):
        t = _TestDefaults(default_int=1, default_float=0.1, default_bool=False, default_string='abc', default_object=['xyz'], default_int2='abc', other_value=self)
        self.assertEqual(t.default_int, 1)
        self.assertEqual(t.default_float, 0.1)
        self.assertEqual(t.default_bool, False)
        self.assertEqual(t.default_string, 'abc')
        self.assertEqual(t.default_object[0], 'xyz')
        self.assertEqual(t.other_value, self)

    def test_init_from(self):
        t0 = _TestDefaults()
        t0.default_int = 321
        t1 = _TestDefaults(t0)
        self.assertEqual(t1.default_int, 321)

    def test_subscript1(self):
        t = _TestDefaults()
        self.assertEqual(t['default_int'], 123)

    def test_subscript2(self):
        t = _TestDefaults()
        t['default_int'] = 321
        self.assertEqual(t['default_int'], 321)

    def test_tmp1(self):
        t = _TestDefaults()
        self.assertFalse('default_int' in _TestDefaults.tmp_fields)
        self.assertTrue('tmp_int' in _TestDefaults.tmp_fields)
        self.assertEqual(t.tmp_int, 50)

    def test_value(self):
        t = _TestDefaults()
        t.default_int = 2
        t.default_float = 0.2
        t.default_bool = False
        t.default_string = 'xyz'
        t.default_object = ['123']
        t.other_value = self
        self.assertEqual(t.default_int, 2)
        self.assertEqual(t.default_float, 0.2)
        self.assertEqual(t.default_bool, False)
        self.assertEqual(t.default_string, 'xyz')
        self.assertEqual(t.default_object[0], '123')
        self.assertEqual(t.other_value, self)
        t.default_object = self
        self.assertEqual(t.default_object[0], '123')

    def test_min(self):
        t = _TestDefaults()
        t.default_int = -1
        t.default_float = 0.0
        self.assertEqual(t.default_int, 0)
        self.assertEqual(t.default_float, 0.1)

    def test_max(self):
        t = _TestDefaults()
        t.default_int = 12345
        t.default_float = 1.0
        self.assertEqual(t.default_int, 999)
        self.assertEqual(t.default_float, 0.9)

    def test_eq1(self):
        t1 = _TestDefaults()
        t2 = _TestDefaults()
        self.assertEqual(t1, t2)

    def test_eq2(self):
        t1 = _TestDefaults()
        t2 = _TestDefaults(default_int=999)
        self.assertNotEqual(t1, t2)

    def test_eq3(self):
        t1 = _TestDefaults()
        t2 = [1, 2, 3]
        self.assertNotEqual(t1, t2)

    def test_eq4(self):
        t1 = _TestDefaults()
        t2 = _TestDefaults(a_val=123)
        self.assertNotEqual(t1, t2)
