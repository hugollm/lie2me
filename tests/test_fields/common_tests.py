from unittest import TestCase

from lie2me import Field
from lie2me.exceptions import FieldValidationError


class CommonTests(object):

    def test_optional_field_against_none_value(self):
        field = self.Field(required=False)
        value, error = field.submit(None)
        self.assertEqual(field.submit(None), (None, None))

    def test_optional_field_against_empty_string(self):
        field = self.Field(required=False)
        self.assertEqual(field.submit(''), (None, None))

    def test_optional_field_against_invisible_characters(self):
        field = self.Field(required=False)
        self.assertEqual(field.submit('  \r\n  '), (None, None))

    def test_required_field_against_none_value(self):
        field = self.Field(required=True)
        value, error = field.submit(None)
        self.assertEqual(error, 'This is required.')

    def test_required_field_against_empty_string(self):
        field = self.Field(required=True)
        value, error = field.submit('')
        self.assertEqual(error, 'This is required.')

    def test_required_field_against_invisible_characters(self):
        field = self.Field(required=True)
        value, error = field.submit('  \r\n  ')
        self.assertEqual(error, 'This is required.')

    def test_field_is_required_by_default(self):
        field = self.Field()
        value, error = field.submit(None)
        self.assertEqual(error, 'This is required.')

    def test_field_with_default_is_never_required(self):
        field = Field(default=self.valid_default, required=True)
        self.assertEqual(field.submit(None), field.submit(self.valid_default))

    def test_field_with_default_against_none_value(self):
        field = self.Field(default=self.valid_default)
        self.assertEqual(field.submit(None), field.submit(self.valid_default))

    def test_field_with_default_against_empty_string(self):
        field = self.Field(default=self.valid_default)
        self.assertEqual(field.submit(''), field.submit(self.valid_default))

    def test_field_with_default_against_invisible_characters(self):
        field = self.Field(default=self.valid_default)
        self.assertEqual(field.submit('  \r\n  '), field.submit(self.valid_default))

    def test_field_instance_can_overwrite_specific_messages(self):
        field = self.Field(messages={'required': 'Lorem ipsum'})
        value, error = field.submit(None)
        self.assertEqual(error, 'Lorem ipsum')
