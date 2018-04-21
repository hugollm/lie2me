from ..field import Field


class Password(Field):

    min = None
    max = None

    messages = {
        'min': 'Must be at least {min} characters long.',
        'max': 'Must have no more than {max} characters.',
    }

    def is_empty(self, value):
        return value is None or value is ''

    def validate(self, value):
        value = str(value)
        if self.min is not None and len(value) < self.min:
            raise self.error('min')
        if self.max is not None and len(value) > self.max:
            raise self.error('max')
        return value
