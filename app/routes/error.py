from utils.validator_helper import create_errors
from bottle import HTTPError, response
from json import dumps, loads


def _error_handler(error: HTTPError):
    try:
        errors = loads(error.body)
        errors = error.body
    except:
        errors = dumps(create_errors('Server', error.body))

    response.status = error.status
    response.set_header('content-type', 'application/json')
    return errors


def _internal_server_error(_):
    response.status = 500
    response.set_header('content-type', 'application/json')
    return dumps(create_errors('Server', 'Internal Server Error.'))


error_handler = {
    400: _error_handler,
    401: _error_handler,
    404: _error_handler,
    409: _error_handler,
    500: _internal_server_error
}
