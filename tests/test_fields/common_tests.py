from unittest import TestCase

from lie2me import Field
from lie2me.exceptions import FieldValidationError


class CommonTests(object):

    def test_optional_field_against_none_value(self):
        field = self.Field(required=False)
        self.assertEqual(field.validate(None), None)

    def test_required_field_against_none_value(self):
        field = self.Field(required=True)
        with self.assertRaises(FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.data, 'This field is required')

    def test_field_is_required_by_default(self):
        field = self.Field()
        with self.assertRaises(FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.data, 'This field is required')

    def test_field_with_default_is_never_required(self):
        field = Field(default=42, required=True)
        value = field.validate(None)
        self.assertEqual(value, 42)

    def test_field_with_default_against_none_value(self):
        field = self.Field(default=42)
        value = field.validate(None)
        self.assertEqual(value, 42)

    def test_field_instance_can_overwrite_specific_messages(self):
        field = self.Field(messages={'required': 'Lorem ipsum'})
        with self.assertRaises(FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.data, 'Lorem ipsum')
