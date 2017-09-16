from datetime import time, timedelta
from unittest import TestCase

from lie2me.fields import Time
from lie2me.exceptions import FieldValidationError

from .common_tests import CommonTests


class TimeTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Time
        self.valid_default = '21:06'

    def test_native_time_object_is_valid(self):
        field = Time()
        value = field.validate(time(21, 6))
        self.assertEqual(value, time(21, 6))

    def test_valid_naive_time_without_seconds(self):
        field = Time()
        value = field.validate('21:06')
        self.assertEqual(value, time(21, 6))

    def test_valid_naive_time_with_seconds(self):
        field = Time()
        value = field.validate('21:06:32')
        self.assertEqual(value, time(21, 6, 32))

    def test_valid_aware_time(self):
        field = Time()
        value = field.validate('21:06-03:00')
        self.assertEqual(value.utcoffset(), timedelta(hours=-3))
        self.assertEqual(value.replace(tzinfo=None), time(21, 6))

    def test_forbidden_naive_time(self):
        field = Time(naive=False)
        with self.assertRaises(FieldValidationError) as context:
            field.validate('21:06')
        self.assertEqual(context.exception.data, 'Requires timezone information.')

    def test_forbidden_aware_time(self):
        field = Time(naive=True)
        with self.assertRaises(FieldValidationError) as context:
            field.validate('21:06-03:00')
        self.assertEqual(context.exception.data, 'Must not have timezone information.')

    def test_invalid_time_format(self):
        field = Time()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('invalid')
        self.assertEqual(context.exception.data, 'Invalid time.')

    def test_invalid_time(self):
        field = Time()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('24:00')
        self.assertEqual(context.exception.data, 'Invalid time.')

    def test_min_constraint(self):
        field = Time(min='05:00')
        with self.assertRaises(FieldValidationError) as context:
            field.validate('04:59')
        self.assertEqual(context.exception.data, 'Must not come before 05:00.')

    def test_max_constraint(self):
        field = Time(max='05:00')
        with self.assertRaises(FieldValidationError) as context:
            field.validate('05:01')
        self.assertEqual(context.exception.data, 'Must not come after 05:00.')

    def test_invalid_min_constraint_fails_at_field_construction(self):
        with self.assertRaises(ValueError):
            Time(min='invalid')

    def test_invalid_max_constraint_fails_at_field_construction(self):
        with self.assertRaises(ValueError):
            Time(max='invalid')

    def test_none_value_is_kept_if_field_is_optional(self):
        field = Time(required=False)
        self.assertEqual(field.validate(None), None)
