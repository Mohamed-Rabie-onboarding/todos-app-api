import py_dotenv
import os
from os.path import join, dirname
from bottle import Bottle
# from database.db import create_db_plugin
# from utils.patch_mount import patch_mount

from routes.user import userRoutes
# from routes.collection import collectionRoutes
# from routes.todo import todoRoutes
from routes.error import errorRoutes


def main():
    app = Bottle()

    # patch mount function to install plugins on sub-apps
    # patch_mount(app)

    # load dotenv file only in development mode
    development = bool(os.getenv('DEV'))
    if development:
        path = join(dirname(__file__), '..', '.env')
        py_dotenv.read_dotenv(path)

    # envs
    port = int(os.getenv('PORT'))
    # dbUri = os.getenv('DB_URL')

    # register plugins
    # app.install(create_db_plugin(dbUri))

    # register routes
    app.mount('/api/v1/user', userRoutes)
    # app.mount('/api/v1/collection', collectionRoutes)
    # app.mount('/api/v1/todo', todoRoutes)
    app.merge(errorRoutes)

    # run the app
    app.run(
        debug=development,
        port=port,
        reloader=development,
    )

    return app


if __name__ == '__main__':
    main()
