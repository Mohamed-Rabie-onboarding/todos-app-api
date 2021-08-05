from utils.getBody import get_body
from utils.error import Error, error_item
from re import match
from types import FunctionType

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


def validate_body(fields: dict):
    body: dict = get_body()
    errors = []

    for key, valdiator in fields.items():
        field = body.get(key)
        if field is None:
            if type(valdiator) == FunctionType or (type(valdiator) == dict and valdiator.get('required') == True):
                errors.append(error_item(
                    field=key, message='Field is required.'))
            continue

        fn = None
        if type(valdiator) == FunctionType:
            fn = valdiator
        elif type(valdiator) == dict and type(valdiator.get('fn')) == FunctionType:
            fn = valdiator.get('fn')
        elif type(valdiator) == dict and valdiator.get('required') == False:
            continue

        value = valdiator(field)
        if value['valid'] == False:
            errors.append(error_item(field=key, message=value['message']))

    if len(errors) != 0:
        raise Error(errors=errors)
    return body
