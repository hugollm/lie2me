from unittest import TestCase

from lie2me.fields import Boolean
from lie2me.exceptions import FieldValidationError


class BooleanTestCase(TestCase):

    def test_value_is_converted_to_boolean(self):
        field = Boolean()
        value = field.validate(42)
        self.assertIsInstance(value, bool)

    def test_false_value_is_not_interpreted_as_none(self):
        field = Boolean()
        value = field.validate(False)
        self.assertEqual(value, False)

    def test_inherited_required_configuration(self):
        field = Boolean()
        with self.assertRaises(FieldValidationError) as context:
            value = field.validate(None)
        self.assertEqual(context.exception.data, 'This field is required')

    def test_none_value_is_kept_if_field_is_optional(self):
        field = Boolean(required=False)
        self.assertEqual(field.validate(None), None)

    def test_inherited_default_configuration(self):
        field = Boolean(default=False)
        self.assertEqual(field.validate(None), False)
