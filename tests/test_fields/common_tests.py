from unittest import TestCase

from lie2me import Field
from lie2me.exceptions import FieldValidationError


class CommonTests(object):

    def test_optional_field_against_none_value(self):
        field = self.Field(required=False)
        self.assertEqual(field.submit(None), None)

    def test_optional_field_against_empty_string(self):
        field = self.Field(required=False)
        self.assertEqual(field.submit(''), None)

    def test_optional_field_against_invisible_characters(self):
        field = self.Field(required=False)
        self.assertEqual(field.submit('  \r\n  '), None)

    def test_required_field_against_none_value(self):
        field = self.Field(required=True)
        with self.assertRaises(FieldValidationError) as context:
            field.submit(None)
        self.assertEqual(context.exception.data, 'This is required.')

    def test_required_field_against_empty_string(self):
        field = self.Field(required=True)
        with self.assertRaises(FieldValidationError) as context:
            field.submit('')
        self.assertEqual(context.exception.data, 'This is required.')

    def test_required_field_against_invisible_characters(self):
        field = self.Field(required=True)
        with self.assertRaises(FieldValidationError) as context:
            field.submit('  \r\n  ')
        self.assertEqual(context.exception.data, 'This is required.')

    def test_field_is_required_by_default(self):
        field = self.Field()
        with self.assertRaises(FieldValidationError) as context:
            field.submit(None)
        self.assertEqual(context.exception.data, 'This is required.')

    def test_field_with_default_is_never_required(self):
        field = Field(default=self.valid_default, required=True)
        value = field.submit(None)
        self.assertEqual(value, field.submit(self.valid_default))

    def test_field_with_default_against_none_value(self):
        field = self.Field(default=self.valid_default)
        value = field.submit(None)
        self.assertEqual(value, field.submit(self.valid_default))

    def test_field_with_default_against_empty_string(self):
        field = self.Field(default=self.valid_default)
        value = field.submit('')
        self.assertEqual(value, field.submit(self.valid_default))

    def test_field_with_default_against_invisible_characters(self):
        field = self.Field(default=self.valid_default)
        value = field.submit('  \r\n  ')
        self.assertEqual(value, field.submit(self.valid_default))

    def test_field_instance_can_overwrite_specific_messages(self):
        field = self.Field(messages={'required': 'Lorem ipsum'})
        with self.assertRaises(FieldValidationError) as context:
            field.submit(None)
        self.assertEqual(context.exception.data, 'Lorem ipsum')
