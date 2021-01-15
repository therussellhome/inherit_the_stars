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

class _TestDefaults(defaults.Defaults):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
_TestDefaults.set_defaults(_TestDefaults, _defaults)

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

    def test_subscript1(self):
        t = _TestDefaults()
        self.assertEqual(t['default_int'], 123)

    def test_subscript2(self):
        t = _TestDefaults()
        t['default_int'] = 321
        self.assertEqual(t['default_int'], 321)

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
