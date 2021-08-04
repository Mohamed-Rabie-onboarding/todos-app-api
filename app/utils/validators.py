from utils.error import Error, error_item
from re import match

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def is_email(email: str) -> bool:
    return {
        'valid': match(EMAIL_REGEX, email),
        'message': 'Email address is invalid.'
    }


def is_min_length(length: int):
    def next(str: str):
        return {
            'valid': len(str) >= length,
            'message': 'Too short value.'
        }
    return next


def validate(fields: dict, body: dict):
    errors = []

    for key, valdiator in fields.items():
        value = valdiator(body[key])

        if value['valid'] == False:
            errors.append(error_item(field=key, message=value['message']))

    if len(errors) != 0:
        raise Error(errors=errors)
