from unittest import TestCase

from lie2me.fields import Password
from lie2me.exceptions import FieldValidationError

from .common_tests import CommonTests


class PasswordTestCase(TestCase):

    def setUp(self):
        self.Field = Password

    def test_valid_password(self):
        field = Password()
        value = field.validate('123456')
        self.assertEqual(value, '123456')

    def test_passwords_are_not_trimmed(self):
        field = Password()
        value = field.validate('  123456  ')
        self.assertEqual(value, '  123456  ')

    def test_values_are_converted_to_string(self):
        field = Password()
        value = field.validate(42)
        self.assertEqual(value, '42')

    def test_min_constraint(self):
        field = Password(min=3)
        with self.assertRaises(FieldValidationError) as context:
            field.validate('ab')
        self.assertEqual(context.exception.data, 'Must be at least 3 characters long.')

    def test_max_constraint(self):
        field = Password(max=5)
        with self.assertRaises(FieldValidationError) as context:
            field.validate('foobar')
        self.assertEqual(context.exception.data, 'Must have no more than 5 characters.')

    def test_none_value_is_kept_if_field_is_optional(self):
        field = Password(required=False)
        self.assertEqual(field.validate(None), None)

    def test_default_value_is_respected(self):
        field = Password(default='foobar')
        value = field.validate('')
        self.assertEqual(value, 'foobar')

    def test_default_value_is_not_returned_if_password_is_made_of_spaces(self):
        field = Password(default='foobar')
        value = field.validate('  ')
        self.assertEqual(value, '  ')

    def test_required_error_is_raised_if_password_is_empty_string(self):
        field = Password()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('')
        self.assertEqual(context.exception.data, 'This is required.')

    def test_required_error_is_not_raised_if_password_is_made_of_spaces(self):
        field = Password()
        value = field.validate('  ')
        self.assertEqual(value, '  ')

    def test_password_can_contain_line_breaks(self):
        field = Password()
        value = field.validate('foo\r\nbar')
        self.assertEqual(value, 'foo\r\nbar')

    def test_empty_text_is_normalized_to_none_if_field_is_empty(self):
        field = Password(required=False)
        value = field.validate('')
        self.assertEqual(value, None)

    def test_empty_text_is_not_validated_against_constraints_if_field_is_optional(self):
        field = Password(required=False, min=1)
        field.validate('')
