import os


def load_env_if_dev():
    """ load_env_if_dev checks if app running on dev mode
        if so it loads up the env variable file
    """
    from os.path import join, dirname
    development = bool(os.getenv('DEV'))
    if development:
        import py_dotenv
        path = join(dirname(__file__), '..', '.env')
        py_dotenv.read_dotenv(path)
    return development


def serve():
    """ Calling serve function creates new `Bottle` app
        and loads dotenv if development mode is on (DEV=True)
        and loads routes and register it to the main app
        and starts listen to port ($PORT)
        and returns the app instance
    """
    from bottle import Bottle

    main_app = Bottle()

    # import & register routes
    from app.routes.error import error_handler
    from app.routes.user import userRoutes
    from app.routes.collection import collectionRoutes
    from app.routes.todo import todoRoutes
    from app.routes.todo_item import todoItemRoutes
    from app.routes.docs import docsRoutes

    main_app.error_handler = error_handler
    main_app.mount('/api/v1/user', userRoutes)
    main_app.mount('/api/v1/collection', collectionRoutes)
    main_app.mount('/api/v1/todo', todoRoutes)
    main_app.mount('/api/v1/todo-item', todoItemRoutes)
    main_app.mount('/api/v1/docs', docsRoutes)

    return main_app
