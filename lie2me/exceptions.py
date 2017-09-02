class FieldValidationError(Exception):

    def __init__(self, message):
        self.message = message


class FieldAbortValidation(Exception):

    def __init__(self, value):
        self.value = value
