from bottle import abort
from pydantic import validate_email, ValidationError


def _create_error(field: str, message: str):
    return {'field': field, 'message': message}


def create_errors(field: str, message: str):
    return {
        'errors': [_create_error(field, message)]
    }


def not_found_error(field: str):
    abort(404, create_errors('Server', f'{field} not found.'))


def error_if_not_found(item, field: str):
    if item is None or item == False:
        not_found_error(field)


class ValidatorHelper:
    field: str
    value: str

    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value.strip()

    def is_not_empty(self):
        if self.value is None or self.value == '':
            raise ValueError(f'{self.field} is required.')

        return self

    def is_bool(self):
        if type(self.value) is not bool:
            raise ValueError(f'{self.field} must be boolean.')

        return self

    def has_min_length(self, n: int):
        if len(self.value) < n:
            raise ValueError(f'{self.field} must be more than {n - 1} chars.')

        return self

    def has_max_length(self, n: int):
        if len(self.value) > n:
            raise ValueError(f'{self.field} must be less than {n + 1} chars.')

        return self

    def is_email_format(self):
        if not validate_email(self.value):
            raise ValueError(f'{self.field} is not correct.')

        return self

    def get_value(self):
        return self.value

    @staticmethod
    def format_errors(ve: ValidationError):
        errors = []

        for error in ve.errors():
            errors.append(
                _create_error(error['loc'][0], error['msg'])
            )

        return {'errors': errors}
