from bottle import Bottle, request
from database.models.user import User


def userRoutes(app: Bottle):

    @app.get('/')
    def index():
        return 'working?! 2'

    @app.post('/register')
    def register_handler():
        body = request.body.getvalue()
        user: User = body.decode('utf-8')

        
        return 'registering'
