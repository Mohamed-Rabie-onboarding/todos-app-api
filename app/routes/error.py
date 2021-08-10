from utils.validator_helper import create_errors
from bottle import HTTPError, response, abort


def _error_handler(error: HTTPError):
    response.status = error.status_code
    return error.body


def _internal_server_error(_):
    abort(500, create_errors('Server', 'Internal Server Error.'))


error_handler = {
    400: _error_handler,
    401: _error_handler,
    404: _error_handler,
    409: _error_handler,
    500: _internal_server_error
}
