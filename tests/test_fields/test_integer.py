from unittest import TestCase

from lie2me.fields import Integer
from .common_tests import CommonTests


class IntegerTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Integer
        self.valid_default = 42

    def test_string_value_is_converted_to_integer(self):
        field = Integer()
        value, error = field.submit('42')
        self.assertEqual(value, 42)

    def test_invalid_integer(self):
        field = Integer()
        value, error = field.submit('foobar')
        self.assertEqual(error, 'Invalid number.')

    def test_invalid_integer_when_passing_unexpected_type(self):
        field = Integer()
        value, error = field.submit([])
        self.assertEqual(error, 'Invalid number.')

    def test_min_constraint(self):
        field = Integer(min=3)
        value, error = field.submit(2)
        self.assertEqual(error, 'Must not be lower than 3.')

    def test_max_constraint(self):
        field = Integer(max=99)
        value, error = field.submit(100)
        self.assertEqual(error, 'Must not be higher than 99.')
