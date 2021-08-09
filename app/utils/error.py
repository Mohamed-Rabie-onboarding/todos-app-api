from typing import List


def is_not_empty(v: str, field: str):
    v = v.strip()
    if v is None or v == '':
        raise ValueError(f'{field} is required.')
    return v


def error_item(field: str, message: str):
    return {'field': field, 'message': message}


def system_error_item(message: str):
    return {'field': '$System', 'message': message}


class Error(Exception):

    def __init__(self, errors: List[dict]):
        self.errors = errors
