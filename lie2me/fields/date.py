from dateutil.parser import parse
from ..field import Field


class Date(Field):

    min = None
    max = None
    dayfirst = False

    messages = {
        'type': 'Invalid date.',
        'min': 'Must not come before {min}.',
        'max': 'Must not come after {max}.',
    }

    def __init__(self, *args, **kwargs):
        super(Date, self).__init__(*args, **kwargs)
        self.parsed_min = self.parse(self.min).date() if self.min else None
        self.parsed_max = self.parse(self.max).date() if self.max else None

    def validation(self, value):
        value = super(Date, self).validation(value)
        try:
            value = self.parse(value)
        except:
            raise self.error('type')
        value = value.date()
        if self.min and value < self.parsed_min:
            raise self.error('min')
        if self.max and value > self.parsed_max:
            raise self.error('max')
        return value

    def parse(self, value):
        return parse(value, dayfirst=self.dayfirst)
