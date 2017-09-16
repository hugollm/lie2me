from unittest import TestCase

from lie2me.fields import Boolean
from lie2me.exceptions import FieldValidationError

from .common_tests import CommonTests


class BooleanTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Boolean
        self.valid_default = 'yes'

    def test_true_values(self):
        field = Boolean()
        samples = [True, 'true', 'True', 'yes', 'Yes', 1, '1', 'on', 'On']
        for sample in samples:
            value = field.validate(sample)
            self.assertEqual(value, True)

    def test_false_values(self):
        field = Boolean()
        samples = [False, 'false', 'False', 'no', 'No', 0, '0', 'off', 'Off']
        for sample in samples:
            value = field.validate(sample)
            self.assertEqual(value, False)

    def test_invalid_value(self):
        field = Boolean()
        with self.assertRaises(FieldValidationError) as context:
            field.validate(42)
        self.assertEqual(context.exception.data, 'Invalid boolean')
