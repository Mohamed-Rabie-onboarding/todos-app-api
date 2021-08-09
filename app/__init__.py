import py_dotenv
import os
from os.path import join, dirname
from bottle import Bottle


def main():
    app = Bottle()

    # load dotenv file only in development mode
    development = bool(os.getenv('DEV'))
    if development:
        path = join(dirname(__file__), '..', '.env')
        py_dotenv.read_dotenv(path)

    # import & register routes
    from routes.user import userRoutes
    from routes.collection import collectionRoutes
    # from routes.todo import todoRoutes
    from routes.error import errorRoutes

    app.mount('/api/v1/user', userRoutes)
    app.mount('/api/v1/collection', collectionRoutes)
    # app.mount('/api/v1/todo', todoRoutes)
    app.merge(errorRoutes)

    # run the app
    app.run(
        debug=development,
        port=int(os.getenv('PORT')),
        reloader=development,
    )

    return app


if __name__ == '__main__':
    main()
