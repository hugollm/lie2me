from . import exceptions


class Field(object):

    required = True
    default = None
    messages = {'required': 'This field is required'}

    def __init__(self, *args, **kwargs):
        if args:
            raise exceptions.PositionalArgumentFieldError()
        self.messages = self._assemble_class_messages()
        self._update_attributes(kwargs)

    def _assemble_class_messages(self):
        messages = {}
        for cls in reversed(self.__class__.__mro__):
            if hasattr(cls, 'messages'):
                messages.update(cls.messages)
        return messages

    def _update_attributes(self, kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise exceptions.InvalidFieldArgumentError(self.__class__, key)
            if key == 'messages':
                self.messages.update(value)
            else:
                setattr(self, key, value)

    def validate(self, value):
        try:
            return self.validation(value)
        except exceptions.FieldAbortValidation as e:
            return e.value

    def validation(self, value):
        if self.required and self.default is None and value is None:
            raise self.error('required')
        if value is None:
            raise self.abort(self.default)
        return value

    def error(self, message):
        message = self.messages.get(message, message)
        return exceptions.FieldValidationError(message)

    def abort(self, value):
        raise exceptions.FieldAbortValidation(value)
