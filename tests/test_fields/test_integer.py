from unittest import TestCase

from lie2me.fields import Integer
from lie2me.exceptions import FieldValidationError

from .common_tests import CommonTests


class IntegerTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Integer

    def test_string_value_is_converted_to_integer(self):
        field = Integer()
        value = field.validate('42')
        self.assertEqual(value, 42)

    def test_invalid_integer(self):
        field = Integer()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('foobar')
        self.assertEqual(context.exception.data, 'A valid integer must be provided')

    def test_invalid_integer_when_passing_unexpected_type(self):
        field = Integer()
        with self.assertRaises(FieldValidationError) as context:
            field.validate([])
        self.assertEqual(context.exception.data, 'A valid integer must be provided')

    def test_min_constraint(self):
        field = Integer(min=3)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(2)
        self.assertEqual(context.exception.data, 'Value may not be lesser than 3')

    def test_max_constraint(self):
        field = Integer(max=99)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(100)
        self.assertEqual(context.exception.data, 'Value may not be higher than 99')
