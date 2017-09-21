from datetime import date
from unittest import TestCase

from lie2me.fields import Date
from lie2me.exceptions import FieldValidationError

from .common_tests import CommonTests


class DateTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Date
        self.valid_default = '2017-09-10'

    def test_native_date_object_is_valid(self):
        field = Date()
        value = field.submit(date(2017, 9, 10))
        self.assertEqual(value, date(2017, 9, 10))

    def test_valid_date(self):
        field = Date()
        value = field.submit('2017-09-10')
        self.assertEqual(value, date(2017, 9, 10))

    def test_invalid_format(self):
        field = Date()
        with self.assertRaises(FieldValidationError) as context:
            field.submit('invalid')
        self.assertEqual(context.exception.data, 'Invalid date.')

    def test_invalid_date(self):
        field = Date()
        with self.assertRaises(FieldValidationError) as context:
            field.submit('2017-02-30')
        self.assertEqual(context.exception.data, 'Invalid date.')

    def test_date_format_can_be_configured(self):
        field = Date(format='%d/%m/%Y')
        value = field.submit('10/09/2017')
        self.assertEqual(value, date(2017, 9, 10))

    def test_without_format_configuration_parsing_is_strict(self):
        field = Date()
        with self.assertRaises(FieldValidationError) as context:
            field.submit('2017-9-2')
        self.assertEqual(context.exception.data, 'Invalid date.')

    def test_once_a_format_is_configured_python_native_parsing_takes_place(self):
        field = Date(format='%Y-%m-%d')
        self.assertEqual(field.submit('2017-9-2'), date(2017, 9, 2))

    def test_min_constraint(self):
        field = Date(min='2017-09-11')
        with self.assertRaises(FieldValidationError) as context:
            field.submit('2017-09-10')
        self.assertEqual(context.exception.data, 'Must not come before 2017-09-11.')

    def test_max_constraint(self):
        field = Date(max='2017-09-10')
        with self.assertRaises(FieldValidationError) as context:
            field.submit('2017-09-11')
        self.assertEqual(context.exception.data, 'Must not come after 2017-09-10.')

    def test_min_constraint_is_parsed_with_the_same_format_as_the_value(self):
        field = Date(min='20/09/2017', format='%d/%m/%Y')
        with self.assertRaises(FieldValidationError):
            field.submit('19/09/2017')

    def test_max_constraint_is_parsed_with_the_same_format_as_the_value(self):
        field = Date(max='20/09/2017', format='%d/%m/%Y')
        with self.assertRaises(FieldValidationError):
            field.submit('21/09/2017')

    def test_invalid_min_constraint_fails_at_field_construction(self):
        with self.assertRaises(ValueError):
            Date(min='invalid')

    def test_invalid_max_constraint_fails_at_field_construction(self):
        with self.assertRaises(ValueError):
            Date(max='invalid')
