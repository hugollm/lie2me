from dateutil.parser import parse
from ..field import Field


class DateTime(Field):

    naive = None
    min = None
    max = None
    dayfirst = False

    messages = {
        'type': 'Unknown date format',
        'naive': 'This field requires timezone information',
        'aware': 'This field does not accept timezone information',
        'min': 'This field only accepts values starting from {min}',
        'max': 'This field only accepts values until {max}',
    }

    def __init__(self, *args, **kwargs):
        super(DateTime, self).__init__(*args, **kwargs)
        self.parsed_min = self.parse(self.min) if self.min else None
        self.parsed_max = self.parse(self.max) if self.max else None

    def validation(self, value):
        value = super(DateTime, self).validation(value)
        try:
            value = self.parse(value)
        except:
            raise self.error('type')
        if self.naive is True and value.tzinfo:
            raise self.error('aware')
        if self.naive is False and not value.tzinfo:
            raise self.error('naive')
        if self.min and value < self.parsed_min:
            raise self.error('min')
        if self.max and value > self.parsed_max:
            raise self.error('max')
        return value

    def parse(self, value):
        return parse(value, dayfirst=self.dayfirst)
