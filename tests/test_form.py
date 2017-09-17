from unittest import TestCase

from lie2me import Form, fields
from lie2me.exceptions import BadFormValidationError


class FormTestCase(TestCase):

    def test_form_without_fields_is_always_valid(self):
        form = Form({'foo': 'bar'})
        form.submit()
        self.assertEqual(form.errors, {})

    def test_before_submission_form_valid_attribute_is_none(self):
        form = Form()
        self.assertEqual(form.valid, None)

    def test_form_data_is_accessible_and_unchanged_before_validation(self):
        form = SignupForm({
            'name': 'John Doe',
            'email': 'john.doe@domain.com',
            'password': '123',
            'password2': '123',
        })
        self.assertEqual(form.data, {
            'name': 'John Doe',
            'email': 'john.doe@domain.com',
            'password': '123',
            'password2': '123',
        })

    def test_form_validation_against_valid_data(self):
        form = SignupForm({
            'name': 'John Doe',
            'email': 'john.doe@domain.com',
            'password': '123',
            'password2': '123',
        })
        form.submit()
        self.assertEqual(form.valid, True)
        self.assertEqual(form.errors, {})

    def test_successful_validation_replaces_form_data_with_new_data(self):
        form = SignupForm({
            'name': '  John Doe  ',
            'email': 'john.doe@domain.com',
            'password': '123',
            'password2': '123',
        })
        form.submit()
        self.assertEqual(form.data, {
            'name': 'John Doe',
            'email': 'john.doe@domain.com',
            'password': '123',
            'password2': '123',
            'observations': None,
        })

    def test_unsuccessful_validation_does_not_replace_form_data_with_new_data(self):
        form = SignupForm({
            'name': '  John Doe  ',
        })
        form.submit()
        self.assertEqual(form.data['name'], '  John Doe  ')

    def test_form_validation_against_invalid_data(self):
        form = SignupForm({
            'name': 'a' * 201,
            'email': 'john.doe@domain',
            'password': '123',
            'password2': '1234',
        })
        form.submit()
        self.assertEqual(form.valid, False)
        self.assertEqual(form.errors, {
            'name': 'Must have no more than 200 characters.',
            'email': 'Invalid email.',
            'password2': 'Password confirmation does not match.',
        })

    def test_form_has_no_errors_before_calling_validate_even_if_data_is_invalid(self):
        form = SignupForm({
            'name': 'a' * 201,
            'email': 'john.doe@domain',
            'password': '12',
            'password2': '123',
        })
        self.assertEqual(form.errors, {})

    def test_form_without_errors_returning_none_in_validation_method_raises_exception(self):
        form = BadValidationForm()
        with self.assertRaises(BadFormValidationError):
            form.submit()

    def test_nested_form_empty_data(self):
        form = ProfileForm()
        self.assertEqual(form.data, {'address': {}})

    def test_nested_form_validated_data(self):
        form = ProfileForm({
            'name': 'John Doe',
            'email': 'john.doe@domain.com',
            'address': {
                'street': 'Nowhere Street',
                'number': 42,
            }
        })
        form.submit()
        self.assertEqual(form.valid, True)
        self.assertEqual(form.data, {
            'name': 'John Doe',
            'email': 'john.doe@domain.com',
            'address': {
                'street': 'Nowhere Street',
                'number': 42,
                'complement': None,
            }
        })

    def test_nested_form_errors(self):
        form = ProfileForm({
            'name': 'a' * 201,
            'email': 'john.doe@domain',
            'address': {
                'street': 'a' * 201,
                'number': -1,
            }
        })
        form.submit()
        self.assertEqual(form.valid, False)
        self.assertEqual(form.errors, {
            'name': 'Must have no more than 200 characters.',
            'email': 'Invalid email.',
            'address': {
                'street': 'Must have no more than 200 characters.',
                'number': 'Must not be lower than 0.',
            }
        })

    def test_nested_form_with_error_only_in_nested_form(self):
        form = ProfileForm({
            'name': 'John Doe',
            'email': 'john.doe@domain.com',
            'address': {
                'street': 'Nowhere Street',
                'number': -1,
            }
        })
        form.submit()
        self.assertEqual(form.valid, False)
        self.assertEqual(form.errors, {
            'address': {
                'number': 'Must not be lower than 0.',
            }
        })

    def test_invalid_data_object_gets_replaced_by_no_data(self):
        form = ProfileForm([1, 2, 3])
        self.assertEqual(form.data, {
            'address': {}
        })
        form.submit()
        self.assertEqual(form.valid, False)
        self.assertEqual(form.errors, {
            'name': 'This is required.',
            'email': 'This is required.',
            'address': {
                'street': 'This is required.',
                'number': 'This is required.',
            },
        })

    def test_weird_values_as_data_do_not_cause_exceptions(self):
        form = ProfileForm()
        form.submit()
        form = ProfileForm(None)
        form.submit()
        form = ProfileForm(42)
        form.submit()
        form = ProfileForm([])
        form.submit()
        form = ProfileForm([1, 2, 3])
        form.submit()
        form = ProfileForm({1, 2, 3})
        form.submit()
        form = ProfileForm(object())
        form.submit()


class SignupForm(Form):

    name = fields.Text(max=200)
    email = fields.Email()
    password = fields.Text(min=3, trim=False)
    password2 = fields.Text(trim=False)
    observations = fields.Text(required=False)

    _ignored_field = fields.Text()

    def validate(self, data):
        if 'password' in data and 'password2' in data:
            if data['password'] != data['password2']:
                self.error('password2', 'Password confirmation does not match.')
        return data


class BadValidationForm(Form):

    name = fields.Text(required=False)

    def validate(self, data):
        pass


class AddressForm(Form):

    street = fields.Text(max=200)
    number = fields.Integer(min=0)
    complement = fields.Text(required=False)


class ProfileForm(Form):

    name = fields.Text(max=200)
    email = fields.Email()
    address = AddressForm
