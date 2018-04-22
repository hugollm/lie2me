class ValidationError(Exception):

    def __init__(self, data):
        self.data = data


class PositionalArgumentFieldError(Exception):

    def __init__(self):
        message = 'Positional arguments are not allowed in fields. Use kwargs.'
        super().__init__(message)


class InvalidFieldArgumentError(Exception):

    def __init__(self, field_type, argument_name):
        message = 'Invalid argument ({}) for field: {}'.format(argument_name, field_type.__name__)
        super().__init__(message)


class BadFieldValidationError(Exception):

    def __init__(self):
        message = 'Field validation returned an error instead of raising it.'
        super().__init__(message)


class BadFormValidationError(Exception):

    def __init__(self):
        message = 'Form validation did not return any data. Did you forget to return?'
        super().__init__(message)


class BadFieldConfiguration(Exception):
    pass
