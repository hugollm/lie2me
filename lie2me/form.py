from .field import Field
from .exceptions import FieldValidationError, BadFormValidationError


class Form(object):

    def __init__(self, data=None):
        self.data = data or {}
        self.errors = {}

    def validate(self):
        data = {}
        fields = self._get_fields()
        for key, field in fields.items():
            try:
                value = field.validate(self.data.get(key))
                data[key] = value
            except FieldValidationError as e:
                self.error(key, e.message)
        data = self.validation(data)
        if self.errors:
            return False
        if data is None:
            raise BadFormValidationError()
        self.data = data
        return True

    def _get_fields(self):
        fields = {}
        for key in dir(self):
            if not key.startswith('_'):
                attr = getattr(self, key)
                if isinstance(attr, Field):
                    fields[key] = attr
        return fields

    def validation(self, data):
        return data

    def error(self, key, message):
        self.errors[key] = message
