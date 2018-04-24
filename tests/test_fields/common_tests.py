from unittest import TestCase
from lie2me import Field


class CommonTests(object):

    def get_instance(self):
        return self.Field()

    def test_submitting_empty_value_on_required_field_returns_error(self):
        field = self.get_instance()
        field.required = True
        value, error = field.submit(field.empty_value())
        self.assertTrue(error)

    def test_submitting_empty_value_on_optional_field_does_not_return_error(self):
        field = self.get_instance()
        field.required = False
        value, error = field.submit(field.empty_value())
        self.assertFalse(error)

    def test_field_is_required_by_default(self):
        field = self.get_instance()
        value, error = field.submit(field.empty_value())
        self.assertTrue(error)

    def test_field_with_default_is_not_required(self):
        field = self.get_instance()
        field.default = self.valid_default
        value, error = field.submit(field.empty_value())
        self.assertFalse(error)

    def test_field_instance_can_overwrite_specific_messages(self):
        field = self.get_instance()
        field.messages = {'required': 'Lorem ipsum'}
        value, error = field.submit(None)
        self.assertIn('Lorem ipsum', str(error))
