from .text import Text


class Email(Text):

    max = 254
    pattern = r'^[^@]+@[^@]+\.[^@]+$'

    messages = {
        'pattern': 'Not a valid email address',
    }
