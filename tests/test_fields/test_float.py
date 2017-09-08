from unittest import TestCase

from lie2me.fields import Float
from lie2me.exceptions import FieldValidationError


class FloatTestCase(TestCase):

    def test_valid_float(self):
        field = Float()
        value = field.validate(3.5)
        self.assertEqual(value, 3.5)

    def test_invalid_float(self):
        field = Float()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('a3.5')
            self.assertEqual(context.exception.data, 'A valid float must be provided')

    def test_validated_value_gets_converted_to_float(self):
        field = Float()
        value = field.validate('3.5')
        self.assertEqual(value, 3.5)

    def test_min_constraint(self):
        field = Float(min=2.9)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(2.8)
        self.assertEqual(context.exception.data, 'Value may not be lesser than 2.9')

    def test_max_constraint(self):
        field = Float(max=15.5)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(15.51)
        self.assertEqual(context.exception.data, 'Value may not be higher than 15.5')

    def test_none_value_is_kept_if_field_is_optional(self):
        field = Float(required=False)
        self.assertEqual(field.validate(None), None)
