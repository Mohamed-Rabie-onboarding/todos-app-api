from pydantic import validate_email
from pydantic import ValidationError


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
            errors.append({
                'field': error['loc'][0],
                'message': error['msg']
            })

        return {'errors': errors}

    @staticmethod
    def duplicated_email_error():
        return {
            'errors': [
                {
                    'field': 'email',
                    'message': 'Email is duplicated.'
                }
            ]
        }
