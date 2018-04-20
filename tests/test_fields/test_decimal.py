from decimal import Decimal as D
from unittest import TestCase

from lie2me.fields import Decimal
from lie2me.exceptions import FieldValidationError

from .common_tests import CommonTests


class DecimalTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Decimal
        self.valid_default = 3.6

    def test_native_decimal_object_is_valid(self):
        field = Decimal()
        value, error = field.submit(D('3.6'))
        self.assertEqual(value, D('3.6'))

    def test_valid_decimal(self):
        field = Decimal()
        value, error = field.submit(3.6)
        self.assertEqual(str(value), str(3.6))

    def test_invalid_decimal(self):
        field = Decimal()
        value, error = field.submit('a3.5')
        self.assertEqual(error, 'Invalid number.')

    def test_validated_value_gets_converted_to_decimal(self):
        field = Decimal()
        value, error = field.submit(3.6)
        self.assertIsInstance(value, D)

    def test_min_constraint(self):
        field = Decimal(min=2.9)
        value, error = field.submit(2.8)
        self.assertEqual(error, 'Must not be lower than 2.9.')

    def test_max_constraint(self):
        field = Decimal(max=15.5)
        value, error = field.submit(15.51)
        self.assertEqual(error, 'Must not be higher than 15.5.')

    def test_min_constraint_is_converted_to_decimal(self):
        field = Decimal(min=3.6)
        field.submit(3.6)

    def test_max_constraint_is_converted_to_decimal(self):
        field = Decimal(max=3.3)
        field.submit(3.3)
