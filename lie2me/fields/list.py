from .. import Form, Field
from ..exceptions import FieldValidationError, InvalidListTypeError


class List(Field):

    type = None

    messages = {
        'type': 'A valid list must be provided',
    }

    def __init__(self, type, *args, **kwargs):
        self.type = type
        if not self._type_is_field() and not self._type_is_form():
            raise InvalidListTypeError()
        super(List, self).__init__(*args, **kwargs)

    def _type_is_field(self):
        return isinstance(self.type, Field)

    def _type_is_form(self):
        return isinstance(self.type, type) and issubclass(self.type, Form)

    def validation(self, values):
        if self.required and values is None:
            raise self.error('required')
        elif values is None:
            return []
        if not isinstance(values, list) and not isinstance(values, tuple):
            raise self.error('type')
        if self.required and not values:
            raise self.error('required')
        new_values = []
        errors = {}
        for i, value in enumerate(values):
            if self._type_is_field():
                try:
                    new_value = self.type.validate(value)
                    new_values.append(new_value)
                except FieldValidationError as e:
                    errors[i] = e.data
            if self._type_is_form():
                form = self.type(value)
                if form.validate():
                    new_values.append(form.data)
                else:
                    errors[i] = form.errors
        if errors:
            raise FieldValidationError(errors)
        return new_values

    def error(self, message):
        e = super(List, self).error(message)
        raise FieldValidationError({'global': e.data})