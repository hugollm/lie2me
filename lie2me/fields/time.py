from dateutil.parser import parse
from ..field import Field


class Time(Field):

    naive = None
    min = None
    max = None

    messages = {
        'type': 'Unknown time format',
        'naive': 'This field requires timezone information',
        'aware': 'This field does not accept timezone information',
        'min': 'This field only accepts values starting from {min}',
        'max': 'This field only accepts values until {max}',
    }

    def __init__(self, *args, **kwargs):
        super(Time, self).__init__(*args, **kwargs)
        self.parsed_min = parse(self.min).time() if self.min else None
        self.parsed_max = parse(self.max).time() if self.max else None

    def validation(self, value):
        value = super(Time, self).validation(value)
        try:
            value = parse(value)
        except:
            raise self.error('type')
        tzinfo = value.tzinfo
        value = value.time().replace(tzinfo=tzinfo)
        if self.naive is True and value.tzinfo:
            raise self.error('aware')
        if self.naive is False and not value.tzinfo:
            raise self.error('naive')
        if self.min and value < self.parsed_min:
            raise self.error('min')
        if self.max and value > self.parsed_max:
            raise self.error('max')
        return value
