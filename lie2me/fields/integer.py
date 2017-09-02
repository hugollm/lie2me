from ..field import Field


class Integer(Field):

    min = None
    max = None

    messages = {
        'type': 'A valid integer must be provided',
        'min': 'Value may not be lesser than {min}',
        'max': 'Value may not be higher than {max}',
    }

    def validation(self, value):
        value = super(Integer, self).validation(value)
        try:
            value = int(value)
        except:
            raise self.error('type')
        if self.min is not None and value < self.min:
            raise self.error('min')
        if self.max is not None and value > self.max:
            raise self.error('max')
        return value
