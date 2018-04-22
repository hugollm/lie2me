from .. import Form, Field
from ..exceptions import ValidationError, BadConfiguration


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
            raise BadConfiguration('First argument must be a field instance.')
        self.field = field
        super().__init__(*args, **kwargs)

    def is_empty(self, data):
        return data is None or data == []

    def empty_value(self):
        return []

    def validate(self, data):
        if not isinstance(data, list) and not isinstance(data, tuple):
            raise self.error('type')
        if self.min is not None and len(data) < self.min:
            raise self.error('min')
        if self.max is not None and len(data) > self.max:
            raise self.error('max')
        new_data = []
        errors = {}
        for i, value in enumerate(data):
            value, error = self.field.submit(value)
            if error is None:
                new_data.append(value)
            else:
                errors[i] = error
        if errors:
            raise ValidationError(errors)
        return new_data

    def error(self, message):
        e = super().error(message)
        raise ValidationError({'list': e.data})
