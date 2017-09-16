from unittest import TestCase

from lie2me.fields import Text
from lie2me.exceptions import FieldValidationError

from .common_tests import CommonTests


class TextTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Text
        self.valid_default = 'foobar'

    def test_valid_value(self):
        field = Text()
        value = field.validate('foobar')
        self.assertEqual(value, 'foobar')

    def test_valid_non_string_value(self):
        field = Text()
        value = field.validate(42)
        self.assertEqual(value, '42')

    def test_valid_value_gets_trimmed(self):
        field = Text()
        value = field.validate('  foobar  ')
        self.assertEqual(value, 'foobar')

    def test_validate_none_raises_required_error(self):
        field = Text()
        with self.assertRaises(FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.data, 'This is required.')

    def test_validate_empty_string_raises_required_error(self):
        field = Text()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('')
        self.assertEqual(context.exception.data, 'This is required.')

    def test_string_with_just_spaces_gets_trimmed_and_raises_required_error(self):
        field = Text()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('  ')
        self.assertEqual(context.exception.data, 'This is required.')

    def test_default_value_is_respected(self):
        field = Text(default='foobar')
        value = field.validate('  ')
        self.assertEqual(value, 'foobar')

    def test_min_constraint(self):
        field = Text(min=3)
        with self.assertRaises(FieldValidationError) as context:
            field.validate('ab')
        self.assertEqual(context.exception.data, 'Must be at least 3 characters long.')

    def test_max_constraint(self):
        field = Text(max=5)
        with self.assertRaises(FieldValidationError) as context:
            field.validate('foobar')
        self.assertEqual(context.exception.data, 'Must have no more than 5 characters.')

    def test_text_is_not_trimmed_if_configuration_is_disabled(self):
        field = Text(trim=False)
        value = field.validate('  foobar  ')
        self.assertEqual(value, '  foobar  ')

    def test_pattern_constraint_against_valid_value(self):
        field = Text(pattern=r'^[a-z]+$')
        field.validate('abc')

    def test_pattern_constraint_against_invalid_value(self):
        field = Text(pattern=r'^[a-z]+$')
        with self.assertRaises(FieldValidationError) as context:
            field.validate('abc1')
        self.assertEqual(context.exception.data, 'Invalid format.')

    def test_multiline_values_are_forbidden_by_default(self):
        field = Text()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('foo\nbar')
        self.assertEqual(context.exception.data, 'Must not have more than one line.')

    def test_multiline_with_only_carriage_returns_are_detected(self):
        field = Text()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('foo\rbar')
        self.assertEqual(context.exception.data, 'Must not have more than one line.')

    def test_field_can_be_configured_to_accept_multilines(self):
        field = Text(multiline=True)
        value = field.validate('foo\nbar')
        self.assertEqual(value, 'foo\nbar')

    def test_pattern_against_multiline_value(self):
        field = Text(multiline=True, pattern=r'^foo.+$')
        value = field.validate('foo\nbar')
        self.assertEqual(value, 'foo\nbar')

    def test_empty_text_is_normalized_to_none_if_field_is_empty(self):
        field = Text(required=False)
        value = field.validate('')
        self.assertEqual(value, None)

    def test_empty_text_is_not_validated_against_constraints_if_field_is_optional(self):
        field = Text(required=False, min=1)
        field.validate('')

    def test_options_constraint_against_valid_value(self):
        field = Text(options=['foo', 'bar'])
        value = field.validate('foo')
        self.assertEqual(value, 'foo')

    def test_options_constraint_against_invalid_value(self):
        field = Text(options=['foo', 'bar'])
        with self.assertRaises(FieldValidationError) as context:
            field.validate('biz')
        self.assertEqual(context.exception.data, 'Invalid option.')
