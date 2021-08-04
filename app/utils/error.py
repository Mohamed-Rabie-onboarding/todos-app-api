from typing import List


def error_item(field: str, message: str):
    return {'field': field, 'message': message}


def system_error_item(message: str):
    return {'field': '$System', 'message': message}


class Error(Exception):

    def __init__(self, errors: List[dict]):
        self.errors = errors
