class FieldValidationError(Exception):

    def __init__(self, message):
        self.message = message


class FieldAbortValidation(Exception):

    def __init__(self, value):
        self.value = value


class PositionalArgumentFieldError(Exception):

    def __init__(self):
        message = 'Positional arguments are not allowed in fields. Use kwargs.'
        super(PositionalArgumentFieldError, self).__init__(message)


class InvalidFieldArgumentError(Exception):

    def __init__(self, field_type, argument_name):
        message = 'Invalid argument ({}) for field: {}'.format(argument_name, field_type.__name__)
        super(InvalidFieldArgumentError, self).__init__(message)
