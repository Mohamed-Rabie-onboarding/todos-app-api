import py_dotenv
import os
from os.path import join, dirname
from bottle import Bottle
from database.db import create_db_plugin

from routes.user import userRoutes
from routes.error import errorRoutes
from routes.list import listRoutes


def create_app_instance():
    # read env file globaly
    path = join(dirname(__file__), '..', '.env')
    py_dotenv.read_dotenv(path)
    return Bottle()


if __name__ == '__main__':
    # get app instance
    app = create_app_instance()

    # register db plugin
    app.install(create_db_plugin())

    # register routes
    errorRoutes(app)
    userRoutes(app)
    listRoutes(app)

    # run bottle app with custom configs
    app.run(
        debug=bool(os.getenv('DEV')),
        port=int(os.getenv('PORT')),
        reloader=bool(os.getenv('DEV')),
    )
