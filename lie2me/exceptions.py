class ValidationError(Exception):

    def __init__(self, data):
        self.data = data


class BadConfiguration(Exception):
    pass


class BadValidation(Exception):
    pass
