from bottle import Bottle, HTTPError


errorRoutes = Bottle()


@errorRoutes.error(400)
def bad_request_handler(err: HTTPError):
    return {'error': 'bad_request_handler'}


@errorRoutes.error(404)
def page_not_found(err: HTTPError):
    return {'error': 'page_not_found'}


@errorRoutes.error(405)
def method_not_allowed(err: HTTPError):
    return {'error': 'errmethod_not_allowedor'}


@errorRoutes.error(500)
def internal_server_error(err: HTTPError):
    print('Error', err)
    return {'error': 'internal_server_error'}
