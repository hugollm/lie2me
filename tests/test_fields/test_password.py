from unittest import TestCase

from lie2me.fields import Password
from .common_tests import CommonTests


class PasswordTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Password
        self.valid_default = '123456'

    def test_valid_password(self):
        field = Password()
        value, error = field.submit('123456')
        self.assertEqual(value, '123456')

    def test_passwords_are_not_trimmed(self):
        field = Password()
        value, error = field.submit('  123456  ')
        self.assertEqual(value, '  123456  ')

    def test_values_are_converted_to_string(self):
        field = Password()
        value, error = field.submit(42)
        self.assertEqual(value, '42')

    def test_min_constraint(self):
        field = Password(min=3)
        value, error = field.submit('ab')
        self.assertEqual(error, 'Must be at least 3 characters long.')

    def test_max_constraint(self):
        field = Password(max=5)
        value, error = field.submit('foobar')
        self.assertEqual(error, 'Must have no more than 5 characters.')

    def test_none_value_is_kept_if_field_is_optional(self):
        field = Password(required=False)
        self.assertEqual(field.submit(None), (None, None))

    def test_default_value_is_respected(self):
        field = Password(default='foobar')
        value, error = field.submit('')
        self.assertEqual(value, 'foobar')

    def test_default_value_is_not_returned_if_password_is_made_of_spaces(self):
        field = Password(default='foobar')
        value, error = field.submit('  ')
        self.assertEqual(value, '  ')

    def test_required_error_is_raised_if_password_is_empty_string(self):
        field = Password()
        value, error = field.submit('')
        self.assertEqual(error, 'This is required.')

    def test_required_error_is_not_raised_if_password_is_made_of_spaces(self):
        field = Password()
        value, error = field.submit('  ')
        self.assertEqual(value, '  ')

    def test_password_can_contain_line_breaks(self):
        field = Password()
        value, error = field.submit('foo\r\nbar')
        self.assertEqual(value, 'foo\r\nbar')

    def test_empty_text_is_normalized_to_none_if_field_is_empty(self):
        field = Password(required=False)
        value, error = field.submit('')
        self.assertEqual(value, None)

    def test_empty_text_is_not_validated_against_constraints_if_field_is_optional(self):
        field = Password(required=False, min=1)
        field.submit('')
