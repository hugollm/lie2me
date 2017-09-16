from datetime import datetime, timedelta
from unittest import TestCase

from lie2me.fields import DateTime
from lie2me.exceptions import FieldValidationError

from .common_tests import CommonTests


class DateTimeTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = DateTime
        self.valid_default = '2017-09-10 22:32'

    def test_native_datetime_object_is_valid(self):
        field = DateTime()
        value = field.validate(datetime(2017, 9, 10, 22, 32))
        self.assertEqual(value, datetime(2017, 9, 10, 22, 32))

    def test_valid_naive_datetime(self):
        field = DateTime()
        value = field.validate('2017-09-10 22:32')
        self.assertEqual(value, datetime(2017, 9, 10, 22, 32))

    def test_valid_aware_datetime(self):
        field = DateTime()
        value = field.validate('2017-09-10 22:32-03:00')
        self.assertEqual(value.utcoffset(), timedelta(hours=-3))
        self.assertEqual(value.replace(tzinfo=None), datetime(2017, 9, 10, 22, 32))

    def test_forbidden_naive_datetime(self):
        field = DateTime(naive=False)
        with self.assertRaises(FieldValidationError) as context:
            field.validate('2017-09-10 22:32')
        self.assertEqual(context.exception.data, 'Requires timezone information.')

    def test_forbidden_aware_datetime(self):
        field = DateTime(naive=True)
        with self.assertRaises(FieldValidationError) as context:
            field.validate('2017-09-10 22:32-03:00')
        self.assertEqual(context.exception.data, 'Must not have timezone information.')

    def test_invalid_datetime(self):
        field = DateTime()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('invalid')
        self.assertEqual(context.exception.data, 'Invalid date or time.')

    def test_min_constraint(self):
        field = DateTime(min='2017-09-11')
        with self.assertRaises(FieldValidationError) as context:
            field.validate('2017-09-10 22:32')
        self.assertEqual(context.exception.data, 'Must not come before 2017-09-11.')

    def test_max_constraint(self):
        field = DateTime(max='2017-09-10 22:31')
        with self.assertRaises(FieldValidationError) as context:
            field.validate('2017-09-10 22:32')
        self.assertEqual(context.exception.data, 'Must not come after 2017-09-10 22:31.')

    def test_min_constraint_is_parsed_with_the_same_arguments_as_the_value(self):
        field = DateTime(min='6/5/2017', dayfirst=True)
        field.validate('6/5/2017')

    def test_max_constraint_is_parsed_with_the_same_arguments_as_the_value(self):
        field = DateTime(max='5/6/2017', dayfirst=True)
        field.validate('5/6/2017')

    def test_invalid_min_constraint_fails_at_field_construction(self):
        with self.assertRaises(ValueError):
            DateTime(min='invalid')

    def test_invalid_max_constraint_fails_at_field_construction(self):
        with self.assertRaises(ValueError):
            DateTime(max='invalid')

    def test_month_is_parsed_first_in_ambiguous_date_by_default(self):
        field = DateTime()
        value = field.validate('10/09/2017 22:32')
        self.assertEqual(value, datetime(2017, 10, 9, 22, 32))

    def test_dayfirst_parsing_for_ambiguous_dates_can_be_configured(self):
        field = DateTime(dayfirst=True)
        value = field.validate('10/09/2017 22:32')
        self.assertEqual(value, datetime(2017, 9, 10, 22, 32))
