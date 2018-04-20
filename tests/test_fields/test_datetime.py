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
        value, error = field.submit(datetime(2017, 9, 10, 22, 32))
        self.assertEqual(value, datetime(2017, 9, 10, 22, 32))

    def test_valid_naive_datetime(self):
        field = DateTime()
        value, error = field.submit('2017-09-10 22:32')
        self.assertEqual(value, datetime(2017, 9, 10, 22, 32))

    def test_valid_aware_datetime(self):
        field = DateTime()
        value, error = field.submit('2017-09-10 22:32-03:00')
        self.assertEqual(value.utcoffset(), timedelta(hours=-3))
        self.assertEqual(value.replace(tzinfo=None), datetime(2017, 9, 10, 22, 32))

    def test_enforced_timezone_constraint_against_naive_datetime(self):
        field = DateTime(timezone=True)
        value, error = field.submit('2017-09-10 22:32')
        self.assertEqual(error, 'Requires timezone information.')

    def test_enforced_timezone_constraint_against_aware_datetime(self):
        field = DateTime(timezone=True)
        value, error = field.submit('2017-09-10 22:32-03:00')
        self.assertEqual(value.utcoffset(), timedelta(hours=-3))
        self.assertEqual(value.replace(tzinfo=None), datetime(2017, 9, 10, 22, 32))

    def test_forbidden_timezone_constraint_against_aware_datetime(self):
        field = DateTime(timezone=False)
        value, error = field.submit('2017-09-10 22:32-03:00')
        self.assertEqual(error, 'Must not have timezone information.')

    def test_forbidden_timezone_constraint_against_naive_datetime(self):
        field = DateTime(timezone=False)
        value, error = field.submit('2017-09-10 22:32')
        self.assertEqual(value, datetime(2017, 9, 10, 22, 32))

    def test_invalid_datetime(self):
        field = DateTime()
        value, error = field.submit('invalid')
        self.assertEqual(error, 'Invalid date or time.')

    def test_min_constraint(self):
        field = DateTime(min='2017-09-11 00:00')
        value, error = field.submit('2017-09-10 22:32')
        self.assertEqual(error, 'Must not come before 2017-09-11 00:00.')

    def test_max_constraint(self):
        field = DateTime(max='2017-09-10 22:31')
        value, error = field.submit('2017-09-10 22:32')
        self.assertEqual(error, 'Must not come after 2017-09-10 22:31.')

    def test_invalid_min_constraint_fails_at_field_construction(self):
        with self.assertRaises(ValueError):
            DateTime(min='invalid')

    def test_invalid_max_constraint_fails_at_field_construction(self):
        with self.assertRaises(ValueError):
            DateTime(max='invalid')
