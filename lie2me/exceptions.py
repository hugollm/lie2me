class ValidationError(Exception):

    def __init__(self, data):
        self.data = data


class BadFieldConfiguration(Exception):
    pass


class BadFieldValidationError(Exception):

    def __init__(self):
        message = 'Field validation returned an error instead of raising it.'
        super().__init__(message)


class BadFormValidationError(Exception):

    def __init__(self):
        message = 'Form validation did not return any data. Did you forget to return?'
        super().__init__(message)
