import re
from .text import Text


class Email(Text):

    max = 254

    messages = {
        'type': 'Not a valid email address',
    }

    def validation(self, value):
        value = super(Email, self).validation(value)
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
            raise self.error('type')
        return value
