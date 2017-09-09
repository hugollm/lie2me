from decimal import Decimal as D
from ..field import Field


class Decimal(Field):

    min = None
    max = None

    messages = {
        'type': 'A valid decimal must be provided',
        'min': 'Value may not be lesser than {min}',
        'max': 'Value may not be higher than {max}',
    }

    def validation(self, value):
        value = super(Decimal, self).validation(value)
        try:
            value = D(str(value))
        except:
            raise self.error('type')
        if self.min is not None and value < D(str(self.min)):
            raise self.error('min')
        if self.max is not None and value > D(str(self.max)):
            raise self.error('max')
        return value
