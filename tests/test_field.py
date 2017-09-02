from unittest import TestCase
from lie2me import Field, exceptions


class FieldTestCase(TestCase):

    def test_validate_returns_value(self):
        field = Field()
        value = field.validate(42)
        self.assertEqual(value, 42)

    def test_field_is_required_by_default(self):
        field = Field()
        with self.assertRaises(exceptions.FieldValidationError):
            field.validate(None)

    def test_field_with_a_default_value_is_never_required(self):
        field = Field(default=42)
        value = field.validate(None)
        self.assertEqual(value, 42)

    def test_required_error_message(self):
        field = Field()
        with self.assertRaises(exceptions.FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.message, 'This field is required')

    def test_field_instance_can_overwrite_specific_messages(self):
        field = Field(messages={'required': 'Required field'})
        with self.assertRaises(exceptions.FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.message, 'Required field')

    def test_overwriting_field_instance_message_does_not_change_class_default_messages(self):
        field = Field(messages={'required': 'Required field'})
        self.assertEqual(Field.messages, {'required': 'This field is required'})

    def test_error_message_is_unchanged_if_its_not_a_key_in_the_messages_dictionary(self):
        field = RawMessage()
        with self.assertRaises(exceptions.FieldValidationError) as context:
            field.validate(42)
        self.assertEqual(context.exception.message, 'Raw message.')

    def test_child_field_does_not_need_to_check_for_null_values_if_its_optional(self):
        field = Boolean(required=False)
        value = field.validate(None)
        self.assertEqual(value, None)

    def test_child_field_does_not_need_custom_init_method_to_configure_its_attributes(self):
        field = AutomaticallyConfigured(min=3)
        self.assertEqual(field.min, 3)

    def test_field_does_not_accept_positional_arguments(self):
        with self.assertRaises(exceptions.PositionalArgumentFieldError):
            field = Field(42)

    def test_field_raises_error_if_invalid_configuration_is_set(self):
        with self.assertRaises(exceptions.InvalidFieldArgumentError):
            field = Field(foo=42)


class RawMessage(Field):

    def validate(self, value):
        raise self.error('Raw message.')


class Boolean(Field):

    def validation(self, value):
        value = super(Boolean, self).validation(value)
        return bool(value)


class AutomaticallyConfigured(Field):
    min = 0
