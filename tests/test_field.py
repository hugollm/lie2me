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
        class RawMessage(Field):
            def validation(self, value):
                raise self.error('Raw message.')
        field = RawMessage()
        with self.assertRaises(exceptions.FieldValidationError) as context:
            field.validate(42)
        self.assertEqual(context.exception.message, 'Raw message.')

    def test_child_field_does_not_need_to_check_for_null_values_if_its_optional(self):
        class Boolean(Field):
            def validation(self, value):
                value = super(Boolean, self).validation(value)
                return bool(value)
        field = Boolean(required=False)
        value = field.validate(None)
        self.assertEqual(value, None)

    def test_child_field_does_not_need_custom_init_method_to_configure_its_attributes(self):
        class AutomaticallyConfigured(Field):
            min = 0
        field = AutomaticallyConfigured(min=3)
        self.assertEqual(field.min, 3)

    def test_field_does_not_accept_positional_arguments(self):
        with self.assertRaises(exceptions.PositionalArgumentFieldError):
            field = Field(42)

    def test_field_raises_error_if_invalid_configuration_is_set(self):
        with self.assertRaises(exceptions.InvalidFieldArgumentError):
            field = Field(foo=42)

    def test_allow_child_field_to_translate_one_message_without_touching_the_others(self):
        class OneMessageTranslated(Field):
            messages = {'foo': 'Lorem ipsum dolor sit amet'}
            def validation(self, value):
                value = super(OneMessageTranslated, self).validation(value)
                raise self.error('foo')
        field = OneMessageTranslated()
        with self.assertRaises(exceptions.FieldValidationError) as context:
            field.validate(42)
        self.assertEqual(context.exception.message, 'Lorem ipsum dolor sit amet')
        with self.assertRaises(exceptions.FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.message, 'This field is required')

    def test_child_class_field_messages_overwrite_parent_messages(self):
        class RequiredMessageTranslated(Field):
            messages = {'required': 'Lorem ipsum dolor sit amet'}
        field = RequiredMessageTranslated()
        with self.assertRaises(exceptions.FieldValidationError) as context:
            field.validate(None)
        self.assertEqual(context.exception.message, 'Lorem ipsum dolor sit amet')

    def test_field_can_use_its_arguments_in_messages(self):
        class ArgumentInMessage(Field):
            min = 3
            def validation(self, value):
                raise self.error('Sample attributes: {min} {min} {required}')
        field = ArgumentInMessage()
        with self.assertRaises(exceptions.FieldValidationError) as context:
            field.validate(42)
        self.assertEqual(context.exception.message, 'Sample attributes: 3 3 True')
