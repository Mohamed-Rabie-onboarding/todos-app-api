from bottle import Bottle


def userRoutes(app: Bottle):

    @app.get('/')
    def index():
        return 'working?!'
