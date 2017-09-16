from unittest import TestCase

from lie2me.fields import Float
from lie2me.exceptions import FieldValidationError

from .common_tests import CommonTests


class FloatTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Float
        self.valid_default = 3.5

    def test_valid_float(self):
        field = Float()
        value = field.validate(3.5)
        self.assertEqual(value, 3.5)

    def test_invalid_float(self):
        field = Float()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('a3.5')
            self.assertEqual(context.exception.data, 'Invalid number.')

    def test_validated_value_gets_converted_to_float(self):
        field = Float()
        value = field.validate('3.5')
        self.assertEqual(value, 3.5)

    def test_min_constraint(self):
        field = Float(min=2.9)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(2.8)
        self.assertEqual(context.exception.data, 'Must not be lower than 2.9.')

    def test_max_constraint(self):
        field = Float(max=15.5)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(15.51)
        self.assertEqual(context.exception.data, 'Must not be higher than 15.5.')
