from unittest import TestCase

from lie2me.fields import Email
from lie2me.exceptions import FieldValidationError, InvalidFieldArgumentError

from .common_tests import CommonTests


class EmailTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Email
        self.valid_default = 'foo@bar.com'

    def test_valid_email_passes_validation(self):
        field = Email()
        email = field.submit('foo@bar.com')
        self.assertEqual(email, 'foo@bar.com')

    def test_email_gets_trimmed(self):
        field = Email()
        email = field.submit('  foo@bar.com  ')
        self.assertEqual(email, 'foo@bar.com')

    def test_email_without_at_sign_does_not_pass_validation(self):
        field = Email()
        with self.assertRaises(FieldValidationError) as context:
            field.submit('foobar.com')
        self.assertEqual(context.exception.data, 'Invalid email.')

    def test_email_with_invalid_domain_does_not_pass_validation(self):
        field = Email()
        with self.assertRaises(FieldValidationError) as context:
            field.submit('foo@bar')
        self.assertEqual(context.exception.data, 'Invalid email.')

    def test_email_cannot_be_longer_than_254_characters(self):
        field = Email()
        with self.assertRaises(FieldValidationError) as context:
            field.submit('foo@bar.com' + ('a' * 244))
        self.assertEqual(context.exception.data, 'Invalid email.')

    def test_email_field_does_not_accept_text_field_parameters(self):
        with self.assertRaises(InvalidFieldArgumentError):
            Email(min=3)
