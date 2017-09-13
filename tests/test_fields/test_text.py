from unittest import TestCase

from lie2me.fields import Text
from lie2me.exceptions import FieldValidationError


class TextTestCase(TestCase):

    def test_valid_value(self):
        field = Text()
        value = field.validate('foobar')
        self.assertEqual(value, 'foobar')

    def test_valid_value_gets_trimmed(self):
        field = Text()
        value = field.validate('  foobar  ')
        self.assertEqual(value, 'foobar')

    def test_validate_none_raises_required_error(self):
        field = Text()
        with self.assertRaises(FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.data, 'This field is required')

    def test_validate_empty_string_raises_required_error(self):
        field = Text()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('')
        self.assertEqual(context.exception.data, 'This field is required')

    def test_string_with_just_spaces_gets_trimmed_and_raises_required_error(self):
        field = Text()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('  ')
        self.assertEqual(context.exception.data, 'This field is required')

    def test_default_value_is_respected(self):
        field = Text(default='foobar')
        value = field.validate('  ')
        self.assertEqual(value, 'foobar')

    def test_min_constraint(self):
        field = Text(min=3)
        with self.assertRaises(FieldValidationError) as context:
            field.validate('ab')
        self.assertEqual(context.exception.data, 'Value may not have less than 3 characters')

    def test_max_constraint(self):
        field = Text(max=5)
        with self.assertRaises(FieldValidationError) as context:
            field.validate('foobar')
        self.assertEqual(context.exception.data, 'Value may not have more than 5 characters')

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
        self.assertEqual(context.exception.data, 'Invalid format')
