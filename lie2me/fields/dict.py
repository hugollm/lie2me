from ..field import Field
from ..exceptions import FieldValidationError, BadFieldConfiguration


class Dict(Field):

    def __init__(self, fields=None, *args, **kwargs):
        self.fields = self._validate_fields(fields)
        super().__init__(*args, **kwargs)

    def _validate_fields(self, fields):
        if fields is None:
            fields = {}
        for key, field in fields.items():
            if not isinstance(field, Field):
                raise BadFieldConfiguration('First argument must be a dict of field instances.')
        return fields

    def submit(self, data):
        data, errors = super().submit(data)
        if errors is None:
            errors = {}
        return data, errors

    def is_empty(self, data):
        return data is None or data == {}

    def empty_value(self):
        return {}

    def validate(self, data):
        new_data = {}
        errors = {}
        for key, field in self.fields.items():
            value, error = field.submit(data.get(key))
            if error:
                errors[key] = error
            else:
                new_data[key] = value
        if errors:
            raise FieldValidationError(errors)
        return new_data
