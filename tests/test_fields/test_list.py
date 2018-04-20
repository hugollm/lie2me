from unittest import TestCase

from lie2me import Form
from lie2me.fields import List, Integer, Text
from lie2me.exceptions import FieldValidationError, InvalidListTypeError


class ListTestCase(TestCase):

    def test_cannot_be_instantiated_without_type_argument(self):
        with self.assertRaises(TypeError):
            List()

    def test_can_be_instantiated_with_form_class_as_type(self):
        List(Form)

    def test_can_be_instantiated_with_field_instance_as_type(self):
        List(Integer())

    def test_cannot_be_instantiated_with_form_instance_as_type(self):
        with self.assertRaises(InvalidListTypeError):
            List(Form())

    def test_cannot_be_instantiated_with_field_class_as_type(self):
        with self.assertRaises(InvalidListTypeError):
            List(Integer)

    def test_required_list_against_missing_data(self):
        field = List(Integer())
        value, errors = field.submit(None)
        self.assertEqual(errors, {'list': 'This is required.'})

    def test_required_list_against_empty_list(self):
        field = List(Integer())
        value, errors = field.submit([])
        self.assertEqual(errors, {'list': 'This is required.'})

    def test_optional_list_against_missing_data(self):
        field = List(Integer(), required=False)
        value, errors = field.submit(None)
        self.assertEqual(value, [])

    def test_optional_list_against_empty_list(self):
        field = List(Integer(), required=False)
        value, errors = field.submit([])
        self.assertEqual(value, [])

    def test_default_values_against_none(self):
        field = List(Integer(), default=[1, 2, 3])
        value, errors = field.submit(None)
        self.assertEqual(value, [1, 2, 3])

    def test_default_values_against_empty_list(self):
        field = List(Integer(), default=[1, 2, 3])
        value, errors = field.submit([])
        self.assertEqual(value, [1, 2, 3])

    def test_list_validation_against_valid_list(self):
        field = List(Integer())
        value, errors = field.submit([1, 2, 3])
        self.assertEqual(value, [1, 2, 3])

    def test_list_validation_against_valid_tuple(self):
        field = List(Integer())
        value, errors = field.submit((1, 2, 3))
        self.assertEqual(value, [1, 2, 3])

    def test_list_validation_return_new_cleaned_values_after_validation(self):
        field = List(Text())
        value, errors = field.submit(['  foo  ', 'bar', 'biz'])
        self.assertEqual(value, ['foo', 'bar', 'biz'])

    def test_list_validation_against_invalid_type_number(self):
        field = List(Integer())
        value, errors = field.submit(42)
        self.assertEqual(errors, {'list': 'Invalid list.'})

    def test_list_validation_against_invalid_type_dict(self):
        field = List(Integer())
        value, errors = field.submit({'foo': 'bar'})
        self.assertEqual(errors, {'list': 'Invalid list.'})

    def test_invalid_type_errors_takes_precedence_over_required(self):
        field = List(Integer())
        value, errors = field.submit({})
        self.assertEqual(errors, {'list': 'Invalid list.'})

    def test_invalid_type_errors_takes_precedence_over_default(self):
        field = List(Integer(), default=[1, 2, 3])
        value, errors = field.submit({})
        self.assertEqual(errors, {'list': 'Invalid list.'})

    def test_list_validation_against_invalid_data(self):
        field = List(Integer())
        value, errors = field.submit([1, 'a', 3])
        self.assertEqual(errors, {1: 'Invalid number.'})

    def test_min_constraint_against_valid_data(self):
        field = List(Integer(), min=3)
        value, errors = field.submit([1, 2, 3])
        self.assertEqual(value, [1, 2, 3])

    def test_min_constraint_against_invalid_data(self):
        field = List(Integer(), min=3)
        value, errors = field.submit([1, 2])
        self.assertEqual(errors, {'list': 'Must have at least 3 items.'})

    def test_max_constraint_against_valid_data(self):
        field = List(Integer(), max=3)
        value, errors = field.submit([1, 2, 3])
        self.assertEqual(value, [1, 2, 3])

    def test_max_constraint_against_invalid_data(self):
        field = List(Integer(), max=3)
        value, errors = field.submit([1, 2, 3, 4])
        self.assertEqual(errors, {'list': 'Must have no more than 3 items.'})

    def test_form_list_validation_against_valid_data(self):
        field = List(ProfileForm)
        value, errors = field.submit([
            {'name': 'John Doe', 'age': 32},
            {'name': 'Jane Doe', 'age': 31},
        ])
        self.assertEqual(value, [
            {'name': 'John Doe', 'age': 32},
            {'name': 'Jane Doe', 'age': 31},
        ])

    def test_form_list_validation_against_invalid_data(self):
        field = List(ProfileForm)
        value, errors = field.submit([
            {'age': 18},
            {'name': 'Jane Doe', 'age': 17},
        ])
        self.assertEqual(errors, {
            0: {'name': 'This is required.'},
            1: {'age': 'Must not be lower than 18.'}
        })

    def test_form_list_receives_cleaned_data_after_validation(self):
        field = List(ProfileForm)
        value, errors = field.submit([
            {'name': '  John Doe  ', 'age': 32},
            {'name': 'Jane Doe', 'age': 31},
        ])
        self.assertEqual(value, [
            {'name': 'John Doe', 'age': 32},
            {'name': 'Jane Doe', 'age': 31},
        ])


class ProfileForm(Form):

    name = Text()
    age = Integer(min=18)
