from utils.error import Error, error_item
from bottle import Bottle
from database.models.user import User
from utils.getBody import get_body
import utils.validators as v
from utils.res import json_res
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from pymysql.err import IntegrityError as IE2
import bcrypt


def userRoutes(app: Bottle):

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
            password=bcrypt.hashpw(
                body['password'].encode('utf-8'),
                bcrypt.gensalt(12)
            )
        )

        try:
            db.add(user)
            db.commit()
        except IntegrityError as e:
            x: IE2 = e.orig
            (state, _) = x.args
            if state == 1062:
                raise Error([error_item('email', 'Email is duplicated.')])
            else:
                raise e

        return json_res(data={'message': 'Successfully added new user!'})

    @app.post('/login')
    def login_handler(db: Session):
        return 'login'

    @app.post('/me')
    def me_handler(db: Session):
        return 'me'
