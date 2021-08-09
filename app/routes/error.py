from bottle import Bottle, HTTPError


errorRoutes = Bottle()


@errorRoutes.error(404)
def page_not_found(err: HTTPError):
    return {'error': 'error'}


@errorRoutes.error(405)
def method_not_allowed(err: HTTPError):
    return {'error': 'error'}


@errorRoutes.error(500)
def internal_server_error(err: HTTPError):
    return {'error': 'error'}
