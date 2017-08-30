from .exceptions import FieldValidationError


class Field(object):

    required = True
    default = None
    messages = {'required': 'This field is required'}

    def __init__(self, required=True, default=None, messages=None):
        self.required = required
        self.default = default
        self.messages = self.messages.copy()
        self.messages.update(messages or {})

    def validate(self, value):
        if self.required and self.default is None and value is None:
            raise self.error('required')
        if value is None:
            return self.default
        return value

    def error(self, message):
        message = self.messages.get(message, message)
        return FieldValidationError(message)
