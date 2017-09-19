from dateutil.parser import parse
from ..field import Field


class DateTime(Field):

    timezone = None
    min = None
    max = None
    dayfirst = False

    messages = {
        'type': 'Invalid date or time.',
        'naive': 'Requires timezone information.',
        'aware': 'Must not have timezone information.',
        'min': 'Must not come before {min}.',
        'max': 'Must not come after {max}.',
    }

    def __init__(self, *args, **kwargs):
        super(DateTime, self).__init__(*args, **kwargs)
        self.parsed_min = self.parse(self.min) if self.min else None
        self.parsed_max = self.parse(self.max) if self.max else None

    def validate(self, value):
        value = super(DateTime, self).validate(value)
        try:
            value = self.parse(value)
        except:
            raise self.error('type')
        if self.timezone is True and not value.tzinfo:
            raise self.error('naive')
        if self.timezone is False and value.tzinfo:
            raise self.error('aware')
        if self.min and value < self.parsed_min:
            raise self.error('min')
        if self.max and value > self.parsed_max:
            raise self.error('max')
        return value

    def parse(self, value):
        return parse(value, dayfirst=self.dayfirst)
