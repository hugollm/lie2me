from ..field import Field


class Password(Field):

    min = None
    max = None

    messages = {
        'min': 'Value may not have less than {min} characters',
        'max': 'Value may not have more than {max} characters',
    }

    def validation(self, value):
        if value is not None:
            value = str(value)
        if not value:
            if self.default is not None:
                raise self.abort(self.default)
            if self.required:
                raise self.error('required')
            raise self.abort(None)
        if self.min is not None and len(value) < self.min:
            raise self.error('min')
        if self.max is not None and len(value) > self.max:
            raise self.error('max')
        return value
