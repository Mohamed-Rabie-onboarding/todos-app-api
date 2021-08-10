from bottle import Bottle, static_file
from routes.error import error_handler

docsRoutes = Bottle()
docsRoutes.error_handler = error_handler


@docsRoutes.get('/<filename:re:.*>')
def serve_swagger_ui(filename):
    print(filename)
    return static_file(filename, root='public/')
