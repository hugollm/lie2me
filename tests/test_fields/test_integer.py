from unittest import TestCase

from lie2me.fields import Integer
from lie2me.exceptions import FieldValidationError


class IntegerTestCase(TestCase):

    def test_string_value_is_converted_to_integer(self):
        field = Integer()
        value = field.validate('42')
        self.assertEqual(value, 42)

    def test_invalid_integer(self):
        field = Integer()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('foobar')
        self.assertEqual(context.exception.message, 'A valid integer must be provided')

    def test_min_constraint(self):
        field = Integer(min=3)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(2)
        self.assertEqual(context.exception.message, 'Value may not be lesser than 3')

    def test_max_constraint(self):
        field = Integer(max=99)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(100)
        self.assertEqual(context.exception.message, 'Value may not be higher than 99')

    def test_none_value_is_kept_if_field_is_optional(self):
        field = Integer(required=False)
        self.assertEqual(field.validate(None), None)
