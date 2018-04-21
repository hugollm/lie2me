from .. import Form, Field
from ..exceptions import FieldValidationError, InvalidListTypeError


class List(Field):

    type = None
    min = None
    max = None

    messages = {
        'type': 'Invalid list.',
        'min': 'Must have at least {min} items.',
        'max': 'Must have no more than {max} items.'
    }

    def __init__(self, type, *args, **kwargs):
        self.type = type
        if not self._type_is_field() and not self._type_is_form():
            raise InvalidListTypeError()
        super().__init__(*args, **kwargs)

    def _type_is_field(self):
        return isinstance(self.type, Field)

    def _type_is_form(self):
        return isinstance(self.type, type) and issubclass(self.type, Form)

    def is_empty(self, value):
        return value is None or value == []

    def empty_value(self):
        return []

    def validate(self, values):
        if not isinstance(values, list) and not isinstance(values, tuple):
            raise self.error('type')
        if self.min is not None and len(values) < self.min:
            raise self.error('min')
        if self.max is not None and len(values) > self.max:
            raise self.error('max')
        new_values, errors = self._validate_fields_and_forms(values)
        if errors:
            raise FieldValidationError(errors)
        return new_values

    def _validate_fields_and_forms(self, values):
        new_values = []
        errors = {}
        for i, value in enumerate(values):
            if self._type_is_field():
                new_value, error = self.type.submit(value)
                if error is None:
                    new_values.append(new_value)
                else:
                    errors[i] = error
            if self._type_is_form():
                form = self.type(value)
                form.submit()
                if form.valid:
                    new_values.append(form.data)
                else:
                    errors[i] = form.errors
        return new_values, errors

    def error(self, message):
        e = super().error(message)
        raise FieldValidationError({'list': e.data})
