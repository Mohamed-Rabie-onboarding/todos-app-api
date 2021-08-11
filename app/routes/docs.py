from bottle import Bottle, static_file
from app.routes.error import error_handler

docsRoutes = Bottle()
docsRoutes.error_handler = error_handler


@docsRoutes.get('/<filename:re:.*>')
def serve_swagger_ui(filename):
    """ serve_swagger_ui serve swagger ui files 
        all file should be allocated on public/*.*
    """
    print(filename)
    return static_file(filename, root='public/')
