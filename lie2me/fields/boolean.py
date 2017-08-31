from ..field import Field


class Boolean(Field):

    def validate(self, value):
        value = super(Boolean, self).validate(value)
        if value is None:
            return value
        return bool(value)
