from utils.error import Error, system_error_item
from bottle import Bottle, HTTPError
from utils.res import json_res


def errorRoutes(app: Bottle):

    @app.error(404)
    def page_not_found(err: HTTPError):
        return json_res(errors=[system_error_item('Page Not Found!')])

    @app.error(405)
    def method_not_allowed(err: HTTPError):
        return json_res(errors=[system_error_item('Method Not Allowed')])

    @app.error(500)
    def internal_server_error(err: HTTPError):
        if type(err.exception) == Error:
            return json_res(errors=err.exception.errors)
        return json_res(errors=[system_error_item('Internal Server Error.')])
