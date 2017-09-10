from datetime import date

from unittest import TestCase

from lie2me.fields import Date
from lie2me.exceptions import FieldValidationError


class DateTestCase(TestCase):

    def test_valid_date(self):
        field = Date()
        value = field.validate('2017-09-10')
        self.assertEqual(value, date(2017, 9, 10))

    def test_format_can_be_configured(self):
        field = Date(format='%d/%m/%Y')
        value = field.validate('10/09/2017')
        self.assertEqual(value, date(2017, 9, 10))

    def test_invalid_format(self):
        field = Date()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('2017 09 10')
        self.assertEqual(context.exception.data, 'Invalid date')

    def test_invalid_date(self):
        field = Date()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('2017-02-30')
        self.assertEqual(context.exception.data, 'Invalid date')

    def test_none_value_is_maintained_for_optional_field(self):
        field = Date(required=False)
        self.assertEqual(field.validate(None), None)
