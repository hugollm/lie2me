from ..field import Field


class Integer(Field):

    min = None
    max = None

    messages = {
        'required': 'This field is required',
        'type': 'A valid integer must be provided',
        'min': 'Value is too small',
        'max': 'Value is too high',
    }

    def validation(self, value):
        value = super(Integer, self).validation(value)
        try:
            value = int(value)
        except ValueError:
            raise self.error('type')
        if self.min is not None and value < self.min:
            raise self.error('min')
        if self.max is not None and value > self.max:
            raise self.error('max')
        return value
