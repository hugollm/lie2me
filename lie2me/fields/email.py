import re
from ..field import Field


class Email(Field):

    messages = {
        'type': 'Invalid email.',
    }

    def validate(self, value):
        value = str(value).strip()
        if len(value) > 254:
            raise self.error('type')
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
            raise self.error('type')
        return value
