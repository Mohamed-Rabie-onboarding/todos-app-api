import py_dotenv
import os
from os.path import join, dirname
from bottle import Bottle
from database.db import create_db_plugin

from routes.user import userRoutes


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
    userRoutes(app)

    # run bottle app with custom configs
    app.run(
        debug=bool(os.environ.get('DEV')),
        port=int(os.environ.get('PORT')),
        reloader=bool(os.environ.get('DEV'))
    )
