from typing import Union
from bottle import abort
from pydantic import validate_email, ValidationError


def _create_error(field: str, message: str):
    """ _create_error create an error message

        :param field: what caused the issue if its 
                      internal_server_error the field should be `Server`  
        :param message: the message to be returned for the user
    """
    return {'field': field, 'message': message}


def create_errors(field: str, message: str):
    """ create_errors create an errors response
        using `_create_error`

        :param field: what caused the issue if its 
                      internal_server_error the field should be `Server`  
        :param message: the message to be returned for the user
    """
    return {
        'errors': [_create_error(field, message)]
    }


def not_found_error(field: str):
    """ not_found_error raise an `HTTPError` with code 404
        and with message description what is not found.

        :param field: what is not found.
    """
    abort(404, create_errors('Server', f'{field} not found.'))


def error_if_not_found(item, field: str):
    """ error_if_not_found takes a `maybeNotFoundItem`
        check if its False or None it throws `HTTPError`
        if its not it returns `None`

        :param item: the maybe_not_found_item
        :param field: what might be not found
    """
    if item is None or item == False:
        not_found_error(field)


class ValidatorHelper:
    """ class ValidatorHelper
        provide an interface for verifying body values
        working perfect with `pydantic` package
    """
    field: str
    value: Union[str, bool]

    def __init__(self, field: str, value: Union[str, bool]):
        """ __init__ is the initializar for `ValidatorHelper` class

            :param field: the maybe_not_valid_item
            :param value: the value which should be checked
        """
        t = type(field)
        if t != str and t != bool:
            raise TypeError(f'Expect field of type str/bool but got {t}')
        elif t == str and field.strip() == '':
            raise ValueError('Expected field but got empty string')

        self.field = field.strip()
        self.value = value.strip() if type(value) == str else value

    def is_not_empty(self):
        """ Calling `is_not_empty` means that the value is required
            if `value` is None or empty string ('') it raises `ValueError`
            if `value` passes the validation it returns the class instance 
        """
        if self.value is None or self.value == '':
            raise ValueError(f'{self.field} is required.')

        return self

    def is_bool(self):
        """ Calling `is_bool` means that the value must be a bool
            if `value` is not a valid bool it raises `ValueError`
            if `value` passes the validation it returns the class instance 
        """
        if type(self.value) is not bool:
            raise ValueError(f'{self.field} must be boolean.')

        return self

    def has_min_length(self, n: int):
        """ Calling `has_min_length` means that the value min length should be `n`
            if `value` length is less than n  it raise `ValueError`
            if `value` passes the validation it returns the class instance 

            :param n: the min length of the value
        """
        if len(self.value) < n:
            raise ValueError(f'{self.field} must be more than {n - 1} chars.')

        return self

    def has_max_length(self, n: int):
        """ Calling `has_max_length` means that the value max length should be `n`
            if `value` length is more than n it raise `ValueError`
            if `value` passes the validation it returns the class instance 

            :param n: the max length of the value
        """
        if len(self.value) > n:
            raise ValueError(f'{self.field} must be less than {n + 1} chars.')

        return self

    def is_email_format(self):
        """ Calling `is_email_format` means that the value must be a valid email form
            if `value` is not a valid email form it raise `ValueError`
            if `value` passes the validation it returns the class instance 
        """
        try:
            validate_email(self.value)
        except:
            raise ValueError(f'{self.field} is not correct.')

        return self

    def get_value(self):
        """ get_value return the value passes at initialize
            used after validation as its needed in `pydantic` package
        """
        return self.value

    @staticmethod
    def format_errors(ve: ValidationError):
        """ format_errors formats the errors caused by validators

            :param ve: the validationerror instance
        """
        errors = []

        for error in ve.errors():
            field: str = error['loc'][0]
            msg = error['msg']

            if msg == 'field required':
                msg = f'{field.capitalize()} is required.'

            errors.append(
                _create_error(field, msg)
            )

        return {'errors': errors}
