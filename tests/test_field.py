from unittest import TestCase

from lie2me.field import Field
from lie2me.exceptions import FieldValidationError


class FieldTestCase(TestCase):

    def test_validate_returns_value(self):
        field = Field()
        value = field.validate(42)
        self.assertEqual(value, 42)

    def test_field_is_required_by_default(self):
        field = Field()
        with self.assertRaises(FieldValidationError):
            field.validate(None)

    def test_field_with_a_default_value_is_never_required(self):
        field = Field(default=42)
        value = field.validate(None)
        self.assertEqual(value, 42)

    def test_required_error_message(self):
        field = Field()
        with self.assertRaises(FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.message, 'This field is required')

    def test_field_instance_can_overwrite_specific_messages(self):
        field = Field(messages={'required': 'Required field'})
        with self.assertRaises(FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.message, 'Required field')

    def test_overwriting_field_instance_message_does_not_change_class_default_messages(self):
        field = Field(messages={'required': 'Required field'})
        self.assertEqual(Field.messages, {'required': 'This field is required'})

    def test_error_message_is_unchanged_if_its_not_a_key_in_the_messages_dictionary(self):
        field = RawMessage()
        with self.assertRaises(FieldValidationError) as context:
            field.validate(42)
        self.assertEqual(context.exception.message, 'Raw message.')

    def test_child_field_does_not_need_to_check_for_null_values_if_its_optional(self):
        field = Boolean(required=False)
        value = field.validate(None)
        self.assertEqual(value, None)


class RawMessage(Field):

    def validate(self, value):
        raise self.error('Raw message.')


class Boolean(Field):

    def validation(self, value):
        value = super(Boolean, self).validation(value)
        return bool(value)
