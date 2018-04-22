from ..field import Field
from ..exceptions import FieldValidationError, InvalidDictModelError


class Dict(Field):

    model = None

    def __init__(self, model=None, *args, **kwargs):
        self.model = model
        if self.model is None:
            self.model = {}
        self._validate_model()
        super().__init__(*args, **kwargs)

    def _validate_model(self):
        for key, field in self.model.items():
            if not isinstance(field, Field):
                raise InvalidDictModelError()

    def is_empty(self, value):
        return value is None or value == {}

    def empty_value(self):
        return {}

    def submit(self, data):
        data, errors = super().submit(data)
        if errors is None:
            errors = {}
        return data, errors

    def validate(self, data):
        new_data = {}
        errors = {}
        for key, field in self.model.items():
            value, error = field.submit(data.get(key))
            if error:
                errors[key] = error
            else:
                new_data[key] = value
        if errors:
            raise FieldValidationError(errors)
        return new_data
