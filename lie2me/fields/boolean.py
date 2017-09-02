from ..field import Field


class Boolean(Field):

    def validation(self, value):
        value = super(Boolean, self).validation(value)
        return bool(value)
