from unittest import TestCase
from lie2me import Field, exceptions


class FieldConstructorTestCase(TestCase):

    def test_field_does_not_accept_positional_arguments(self):
        with self.assertRaises(exceptions.PositionalArgumentFieldError):
            field = Field(42)

    def test_field_raises_error_if_invalid_configuration_is_set(self):
        with self.assertRaises(exceptions.InvalidFieldArgumentError):
            field = Field(foo=42)

    def test_child_field_does_not_need_custom_init_method_to_configure_its_attributes(self):
        class AutomaticallyConfigured(Field):
            min = 0
        field = AutomaticallyConfigured(min=3)
        self.assertEqual(field.min, 3)


class FieldSubmitTestCase(TestCase):

    def test_valid_submit_returns_tuple(self):
        field = Field()
        value, error = field.submit(42)
        self.assertEqual(value, 42)
        self.assertEqual(error, None)

    def test_invalid_submit_returns_tuple(self):
        field = Field()
        value, error = field.submit(None)
        self.assertEqual(value, None)
        self.assertEqual(error, 'This is required.')

    def test_skipped_validation_returns_tuple(self):
        field = Field(required=False)
        value, error = field.submit(None)
        self.assertEqual(value, None)
        self.assertEqual(error, None)

    def test_invalid_submit_returns_the_original_value(self):
        class AlwaysInvalid(Field):
            def validate(self, value):
                raise self.error('Invalid!')
        field = AlwaysInvalid()
        input = object()
        value, error = field.submit(input)
        self.assertEqual(value, input)

    def test_returning_error_on_validate_instead_of_raising_triggers_exception(self):
        class InvalidField(Field):
            def validate(self, value):
                return self.error('Invalid!')
        field = InvalidField()
        with self.assertRaises(exceptions.BadFieldValidationError):
            field.submit(42)


class FieldRequiredTestCase(TestCase):

    def test_field_is_required_by_default(self):
        field = Field()
        value, error = field.submit(None)
        self.assertEqual(error, 'This is required.')

    def test_required_error_message(self):
        field = Field()
        value, error = field.submit(None)
        self.assertEqual(error, 'This is required.')

    def test_empty_string_triggers_required_error(self):
        field = Field()
        value, error = field.submit('')
        self.assertEqual(error, 'This is required.')

    def test_string_with_only_spaces_triggers_required_error(self):
        field = Field()
        value, error = field.submit('  ')
        self.assertEqual(error, 'This is required.')

    def test_child_field_does_not_need_to_check_for_null_values_if_its_optional(self):
        class Boolean(Field):
            def validate(self, value):
                value = super().validate(value)
                return bool(value)
        field = Boolean(required=False)
        value, error = field.submit(None)
        self.assertEqual(value, None)

    def test_empty_value_returned_when_field_is_optional_can_be_configured(self):
        class List(Field):
            def empty_value(self):
                return []
        field = List(required=False)
        value, error = field.submit(None)
        self.assertEqual(value, [])
        self.assertEqual(error, None)


class FieldDefaultTestCase(TestCase):

    def test_field_with_a_default_value_is_not_required(self):
        field = Field(default=42)
        value, error = field.submit(None)
        self.assertEqual(value, 42)

    def test_field_default_is_submitted_to_validation(self):
        class IncrementField(Field):
            def validate(self, value):
                value = int(value)
                return value + 1
        field = IncrementField(default='42')
        value, error = field.submit(None)
        self.assertEqual(value, 43)

    def test_field_default_is_submitted_to_validation_even_without_calling_super(self):
        class IncrementField(Field):
            def validate(self, value):
                value = int(value)
                return value + 1
        field = IncrementField(default='42')
        value, error = field.submit(None)
        self.assertEqual(value, 43)


class FieldMessagesTestCase(TestCase):

    def test_field_instance_can_overwrite_specific_messages(self):
        field = Field(messages={'required': 'Required field'})
        value, error = field.submit(None)
        self.assertEqual(error, 'Required field')

    def test_overwriting_field_instance_message_does_not_change_class_default_messages(self):
        field = Field(messages={'required': 'Required field'})
        self.assertEqual(Field.messages, {'required': 'This is required.'})

    def test_error_message_is_unchanged_if_its_not_a_key_in_the_messages_dictionary(self):
        class RawMessage(Field):
            def validate(self, value):
                raise self.error('Raw message.')
        field = RawMessage()
        value, error = field.submit(42)
        self.assertEqual(error, 'Raw message.')

    def test_field_can_use_its_arguments_in_messages(self):
        class ArgumentInMessage(Field):
            min = 3
            def validate(self, value):
                raise self.error('Sample attributes: {min} {min} {required}')
        field = ArgumentInMessage()
        value, error = field.submit(42)
        self.assertEqual(error, 'Sample attributes: 3 3 True')

    def test_allow_child_field_to_translate_one_message_without_touching_the_others(self):
        class OneMessageTranslated(Field):
            messages = {'foo': 'Lorem ipsum dolor sit amet'}
            def validate(self, value):
                value = super().validate(value)
                raise self.error('foo')
        field = OneMessageTranslated()
        value, error = field.submit(42)
        self.assertEqual(error, 'Lorem ipsum dolor sit amet')
        value, error = field.submit(None)
        self.assertEqual(error, 'This is required.')

    def test_child_class_field_messages_overwrite_parent_messages(self):
        class RequiredMessageTranslated(Field):
            messages = {'required': 'Lorem ipsum dolor sit amet'}
        field = RequiredMessageTranslated()
        value, error = field.submit(None)
        self.assertEqual(error, 'Lorem ipsum dolor sit amet')
