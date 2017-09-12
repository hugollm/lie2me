from datetime import date

from unittest import TestCase

from lie2me.fields import Date
from lie2me.exceptions import FieldValidationError


class DateTestCase(TestCase):

    def test_valid_date(self):
        field = Date()
        value = field.validate('2017-09-10')
        self.assertEqual(value, date(2017, 9, 10))

    def test_invalid_format(self):
        field = Date()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('invalid')
        self.assertEqual(context.exception.data, 'Unknown date format')

    def test_invalid_date(self):
        field = Date()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('2017-02-30')
        self.assertEqual(context.exception.data, 'Unknown date format')

    def test_min_constraint(self):
        field = Date(min='2017-09-11')
        with self.assertRaises(FieldValidationError) as context:
            field.validate('2017-09-10')
        self.assertEqual(context.exception.data, 'This field only accepts values starting from 2017-09-11')

    def test_max_constraint(self):
        field = Date(max='2017-09-10')
        with self.assertRaises(FieldValidationError) as context:
            field.validate('2017-09-11')
        self.assertEqual(context.exception.data, 'This field only accepts values until 2017-09-10')

    def test_min_constraint_is_parsed_with_the_same_arguments_as_the_value(self):
        field = Date(min='6/5/2017', dayfirst=True)
        field.validate('6/5/2017')

    def test_max_constraint_is_parsed_with_the_same_arguments_as_the_value(self):
        field = Date(max='5/6/2017', dayfirst=True)
        field.validate('5/6/2017')

    def test_invalid_min_constraint_fails_at_field_construction(self):
        with self.assertRaises(ValueError):
            Date(min='invalid')

    def test_invalid_max_constraint_fails_at_field_construction(self):
        with self.assertRaises(ValueError):
            Date(max='invalid')

    def test_month_is_parsed_first_in_ambiguous_date_by_default(self):
        field = Date()
        value = field.validate('10/09/2017')
        self.assertEqual(value, date(2017, 10, 9))

    def test_dayfirst_parsing_for_ambiguous_dates_can_be_configured(self):
        field = Date(dayfirst=True)
        value = field.validate('10/09/2017')
        self.assertEqual(value, date(2017, 9, 10))

    def test_none_value_is_maintained_for_optional_field(self):
        field = Date(required=False)
        self.assertEqual(field.validate(None), None)
