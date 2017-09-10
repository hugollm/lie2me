from datetime import datetime
from ..field import Field


class Date(Field):

    format = '%Y-%m-%d'

    messages = {
        'type': 'Invalid date',
    }

    def validation(self, value):
        value = super(Date, self).validation(value)
        try:
            value = datetime.strptime(value, self.format).date()
        except:
            raise self.error('type')
        return value
