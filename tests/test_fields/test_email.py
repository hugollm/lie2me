from unittest import TestCase

from lie2me.fields import Email
from lie2me.exceptions import FieldValidationError


class EmailTestCase(TestCase):

    def test_valid_email_passes_validation(self):
        field = Email()
        email = field.validate('foo@bar.com')
        self.assertEqual(email, 'foo@bar.com')

    def test_email_gets_trimmed(self):
        field = Email()
        email = field.validate('  foo@bar.com  ')
        self.assertEqual(email, 'foo@bar.com')

    def test_email_without_at_sign_does_not_pass_validation(self):
        field = Email()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('foobar.com')
        self.assertEqual(context.exception.message, 'Not a valid email address')

    def test_email_with_invalid_domain_does_not_pass_validation(self):
        field = Email()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('foo@bar')
        self.assertEqual(context.exception.message, 'Not a valid email address')

    def test_email_cannot_be_longer_than_254_characters(self):
        field = Email()
        with self.assertRaises(FieldValidationError) as context:
            field.validate('a' * 255)
        self.assertEqual(context.exception.message, 'Value may not have more than 254 characters')
