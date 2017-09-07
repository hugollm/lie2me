from .field import Field
from .exceptions import FieldValidationError, BadFormValidationError


class Form(object):

    def __init__(self, data=None):
        self.fields, self.forms = self._get_fields_and_nested_forms()
        self._initialize_data(data)
        self.errors = {}

    def _get_fields_and_nested_forms(self):
        fields = {}
        forms = {}
        for key in dir(self):
            if not key.startswith('_'):
                attr = getattr(self, key)
                if isinstance(attr, Field):
                    fields[key] = attr
                if isinstance(attr, type) and issubclass(attr, Form):
                    forms[key] = attr
        return fields, forms

    def _initialize_data(self, data):
        self.data = data or {}
        if data is None:
            for key, form in self.forms.items():
                self.data[key] = {}

    def validate(self):
        data = {}
        self._validate_data()
        if not 'global' in self.errors:
            data.update(self._validate_fields())
            data.update(self._validate_forms())
            data = self.validation(data)
        if self.errors:
            return False
        else:
            if data is None:
                raise BadFormValidationError()
            self.data = data
            return True

    def _validate_data(self):
        if not hasattr(self.data, 'get'):
            self.errors['global'] = 'Invalid data'

    def _validate_fields(self):
        data = {}
        for key, field in self.fields.items():
            try:
                value = field.validate(self.data.get(key))
                data[key] = value
            except FieldValidationError as e:
                self.errors[key] = e.data
        return data

    def _validate_forms(self):
        data = {}
        for key, form in self.forms.items():
            f = form(self.data.get(key))
            if f.validate():
                data[key] = f.data
            else:
                self.errors[key] = f.errors
        return data

    def validation(self, data):
        return data

    def error(self, key, message):
        self.errors[key] = message
