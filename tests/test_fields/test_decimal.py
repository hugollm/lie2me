from decimal import Decimal as D

from unittest import TestCase

from lie2me.fields import Decimal
from lie2me.exceptions import FieldValidationError


class DecimalTestCase(TestCase):

    def test_valid_decimal(self):
        field = Decimal()
        value = field.validate(3.6)
        self.assertEqual(str(value), str(3.6))

    def test_invalid_decimal(self):
        field = Decimal()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('a3.5')
        self.assertEqual(context.exception.data, 'A valid decimal must be provided')

    def test_validated_value_gets_converted_to_decimal(self):
        field = Decimal()
        value = field.validate(3.6)
        self.assertIsInstance(value, D)

    def test_min_constraint(self):
        field = Decimal(min=2.9)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(2.8)
        self.assertEqual(context.exception.data, 'Value may not be lesser than 2.9')

    def test_max_constraint(self):
        field = Decimal(max=15.5)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(15.51)
        self.assertEqual(context.exception.data, 'Value may not be higher than 15.5')

    def test_min_constraint_is_converted_to_decimal(self):
        field = Decimal(min=3.6)
        field.validate(3.6)

    def test_max_constraint_is_converted_to_decimal(self):
        field = Decimal(max=3.3)
        field.validate(3.3)

    def test_none_value_is_kept_if_field_is_optional(self):
        field = Decimal(required=False)
        self.assertEqual(field.validate(None), None)
