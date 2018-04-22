import re
from .exceptions import ValidationError, BadConfiguration, BadValidation


class Field(object):

    required = True
    default = None

    messages = {
        'required': 'This is required.',
    }

    def __init__(self, *args, **kwargs):
        if args:
            raise BadConfiguration('Positional arguments are not allowed in this field.')
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
                raise self._invalid_field_argument(key)
            if key == 'messages':
                self.messages.update(value)
            else:
                setattr(self, key, value)

    def _invalid_field_argument(self, key):
        message = 'Invalid argument ({}) for field: {}'.format(key, self.__class__.__name__)
        return BadConfiguration(message)

    def submit(self, value):
        try:
            new_value = self._process_value(value)
        except ValidationError as e:
            return value, e.data
        if isinstance(new_value, ValidationError):
            raise BadValidation('Field validation returned an error instead of raising it.')
        return new_value, None

    def _process_value(self, value):
        if self.default is not None and self.is_empty(value):
            value = self.default
        if self.is_empty(value):
            if self.required:
                raise self.error('required')
            else:
                return self.empty_value()
        return self.validate(value)

    def is_empty(self, value):
        return value is None or str(value).strip() is ''

    def empty_value(self):
        return None

    def validate(self, value):
        return value

    def error(self, message):
        message = self.messages.get(message, message)
        message = self.format_message(message)
        return ValidationError(message)

    def format_message(self, message):
        matches = re.findall(r'\{([a-zA-Z][a-zA-Z0-9_]*?)\}', message)
        for match in matches:
            placeholder = '{' + match + '}'
            message = message.replace(placeholder, str(getattr(self, match)))
        return message
