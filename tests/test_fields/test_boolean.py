from unittest import TestCase

from lie2me.fields import Boolean
from lie2me.exceptions import FieldValidationError

from .common_tests import CommonTests


class BooleanTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Boolean

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
