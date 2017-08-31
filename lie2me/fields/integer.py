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

    def __init__(self, min=None, max=None, *args, **kwargs):
        super(Integer, self).__init__(*args, **kwargs)
        self.min = min
        self.max = max

    def validate(self, value):
        value = super(Integer, self).validate(value)
        if value is None:
            return value
        try:
            value = int(value)
        except ValueError:
            raise self.error('type')
        if self.min is not None and value < self.min:
            raise self.error('min')
        if self.max is not None and value > self.max:
            raise self.error('max')
        return value
