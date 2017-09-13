import re
from ..field import Field


class Text(Field):

    min = None
    max = None
    pattern = None
    trim = True

    messages = {
        'min': 'Value may not have less than {min} characters',
        'max': 'Value may not have more than {max} characters',
        'pattern': 'Invalid format',
    }

    def validation(self, value):
        value = super(Text, self).validation(value)
        value = str(value)
        if self.trim:
            value = value.strip()
        if not value:
            if self.default is not None:
                return self.default
            if self.required:
                raise self.error('required')
        if self.min is not None and len(value) < self.min:
            raise self.error('min')
        if self.max is not None and len(value) > self.max:
            raise self.error('max')
        if self.pattern is not None and not re.match(self.pattern, value):
            raise self.error('pattern')
        return value
