from unittest import TestCase

from lie2me import Field
from lie2me.fields import Dict
from lie2me.exceptions import BadConfiguration
from .common_tests import CommonTests


class DictTestCase(TestCase, CommonTests):

    def setUp(self):
        self.Field = Dict
        self.valid_default = {'foo': 'bar'}

    def get_instance(self):
        return Dict({'foo': Field()})

    def test_field_can_be_constructed_without_arguments(self):
        field = Dict()

    def test_field_can_be_constructed_with_a_dict_of_fields_as_first_argument(self):
        field = Dict({
            'name': Field(),
            'email': Field(),
        })

    def test_field_cannot_be_constructed_with_invalid_dict_of_fields(self):
        with self.assertRaises(BadConfiguration) as context:
            Dict({'name': 'invalid field'})
        self.assertEqual(str(context.exception), 'First argument must be a dict of field instances.')

    def test_empty_data_for_optional_submit_is_an_empty_dict(self):
        field = Dict(required=False)
        data, errors = field.submit(None)
        self.assertEqual(data, {})
        self.assertEqual(errors, {})

    def test_data_submission_against_no_fields_dict_returns_empty_dict_as_data(self):
        field = Dict()
        data, errors = field.submit({'name': 'John Doe'})
        self.assertEqual(data, {})
        self.assertEqual(errors, {})

    def test_data_submit_against_dict_returns_dict_with_only_the_requested_data(self):
        field = Dict({
            'name': Field(),
            'email': Field(),
        })
        data, errors = field.submit({
            'name': 'John Doe',
            'email': 'john.doe@gmail.com',
            'age': 23,
        })
        self.assertEqual(data, {
            'name': 'John Doe',
            'email': 'john.doe@gmail.com',
        })
        self.assertEqual(errors, {})

    def test_invalid_submit_returns_original_data(self):
        field = Dict({
            'name': Field(),
            'email': Field(),
        })
        input_data = {'name': 'John Doe'}
        output_data, errors = field.submit(input_data)
        self.assertIs(output_data, input_data)

    def test_invalid_data_results_in_dictionary_of_specific_errors(self):
        field = Dict({
            'name': Field(),
            'email': Field(),
        })
        data, errors = field.submit({'name': 'John Doe'})
        self.assertEqual(errors, {'email': 'This is required.'})

    def test_nested_dict_fields_return_filtered_data(self):
        field = Dict({
            'name': Field(),
            'address': Dict({
                'street': Field(),
                'number': Field(),
            }),
        })
        data, errors = field.submit({
            'name': 'John Doe',
            'address': {
                'street': 'Some Street',
                'number': 0,
                'filter_this_out': 'lorem ipsum...',
            },
        })
        self.assertEqual(data, {
            'name': 'John Doe',
            'address': {
                'street': 'Some Street',
                'number': 0,
            },
        })
        self.assertEqual(errors, {})

    def test_nested_dict_fields_return_nested_dict_of_errors_on_invalid_submit(self):
        field = Dict({
            'name': Field(),
            'address': Dict({
                'street': Field(),
                'number': Field(),
            }),
        })
        data, errors = field.submit({
            'address': {
                'street': 'Some Street',
                'filter_this_out': 'lorem ipsum...',
            },
        })
        self.assertEqual(data, {
            'address': {
                'street': 'Some Street',
                'filter_this_out': 'lorem ipsum...',
            },
        })
        self.assertEqual(errors, {
            'name': 'This is required.',
            'address': {
                'number': 'This is required.',
            },
        })
