from app.utils.validator_helper import create_errors
from bottle import HTTPError, response
from json import dumps, loads


def _error_handler(error: HTTPError):
    """ _error_handler is the main error handler
        checking if the body of recived error is valid json
        if so it returns it with the attached status_code
        if not it creates new error and returns with with status

        :param error: the HTTPError that cause the fire of this route
    """
    try:
        errors = loads(error.body)
        errors = error.body
    except:
        errors = dumps(create_errors('Server', error.body))

    response.status = error.status
    response.set_header('content-type', 'application/json')
    return errors


def _internal_server_error(_):
    """ _internal_server_error fire whenever unhandled error happen
        creates an error object and returns it as json along with code (500)
    """
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
