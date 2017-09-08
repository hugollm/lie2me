from ..field import Field


class Float(Field):

    min = None
    max = None

    messages = {
        'type': 'A valid float must be provided',
        'min': 'Value may not be lesser than {min}',
        'max': 'Value may not be higher than {max}',
    }

    def validation(self, value):
        value = super(Float, self).validation(value)
        try:
            value = float(value)
        except:
            raise self.error('type')
        if self.min is not None and value < self.min:
            raise self.error('min')
        if self.max is not None and value > self.max:
            raise self.error('max')
        return value
