from utils.error import Error, system_error_item, error_item
from bottle import Bottle, HTTPError
from database.models.user import User
from utils.getBody import get_body
import utils.validators as v
from utils.res import json_res
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from pymysql.err import IntegrityError as IE2


def userRoutes(app: Bottle):

    @app.error(500)
    def internal_server_error(err: HTTPError):
        if type(err.exception) == Error:
            return json_res(errors=err.exception.errors)
        return json_res(errors=[system_error_item('Internal Server Error.')])

    @app.post('/register')
    def register_handler(db: Session):
        body = get_body()

        v.validate({
            'username': v.is_min_length(2),
            'email': v.is_email,
            'password': v.is_min_length(6)
        }, body)

        # user should be valid here
        user = User(
            username=body['username'],
            email=body['email'],
            password=body['password']
        )

        try:
            db.add(user)
            db.commit()
        except IntegrityError as e:
            x: IE2 = e.orig
            (state, _) = x.args
            if state == 1062:
                raise Error([error_item('email', 'Email is duplicated.')])

        return json_res(data={'message': 'Successfully added new user!'})
