import re
from ..field import Field


class Text(Field):

    min = None
    max = None
    multiline = False
    pattern = None
    trim = True

    messages = {
        'min': 'Value may not have less than {min} characters',
        'max': 'Value may not have more than {max} characters',
        'multiline': 'Value may not have more than one line',
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
            return None
        if self.min is not None and len(value) < self.min:
            raise self.error('min')
        if self.max is not None and len(value) > self.max:
            raise self.error('max')
        if not self.multiline and len(value.splitlines()) > 1:
            raise self.error('multiline')
        if self.pattern and not re.match(self.pattern, value, flags=re.MULTILINE|re.DOTALL):
            raise self.error('pattern')
        return value
