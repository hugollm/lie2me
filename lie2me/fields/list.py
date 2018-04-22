from .. import Form, Field
from ..exceptions import FieldValidationError, InvalidListTypeError


class List(Field):

    min = None
    max = None

    messages = {
        'type': 'Invalid list.',
        'min': 'Must have at least {min} items.',
        'max': 'Must have no more than {max} items.',
    }

    def __init__(self, field, *args, **kwargs):
        if not isinstance(field, Field):
            raise InvalidListTypeError()
        self.field = field
        super().__init__(*args, **kwargs)

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
        new_values = []
        errors = {}
        for i, value in enumerate(values):
            new_value, error = self.field.submit(value)
            if error is None:
                new_values.append(new_value)
            else:
                errors[i] = error
        if errors:
            raise FieldValidationError(errors)
        return new_values

    def error(self, message):
        e = super().error(message)
        raise FieldValidationError({'list': e.data})
