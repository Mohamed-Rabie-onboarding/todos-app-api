from bottle import Bottle, HTTPError
from database.models.user import User
from utils.getBody import get_body
import utils.validators as v
from utils.res import json_res


def userRoutes(app: Bottle):

    @app.error(500)
    def internal_server_error(err: HTTPError):
        return json_res(errors=err.exception.errors)

    @app.post('/register')
    def register_handler():
        user = get_body()

        v.validate({
            'username': v.is_min_length(2),
            'email': v.is_email,
            'password': v.is_min_length(6)
        }, user)

        # user should be valid here

        return user
