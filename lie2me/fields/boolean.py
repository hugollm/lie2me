from ..field import Field


class Boolean(Field):

    messages = {
        'type': 'Invalid boolean.',
    }

    def validate(self, value):
        value = str(value).strip().lower()
        if value in ('true', 'yes', '1', 'on'):
            return True
        if value in ('false', 'no', '0', 'off'):
            return False
        raise self.error('type')
