from utils.error import Error, error_item
from bottle import Bottle
from database.models.user import User
import utils.validators as v
from utils.res import json_res
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from pymysql.err import IntegrityError as IE2
import bcrypt
from utils.jwt import sign_token, get_user_id


userRoutes = Bottle()


@userRoutes.post('/register')
def register_handler(db: Session):
    body = v.validate_body({
        'username': v.is_min_length(2),
        'email': v.is_email,
        'password': v.is_min_length(6)
    })

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


@userRoutes.post('/login')
def login_handler(db: Session):
    body = v.validate_body({
        'email': v.is_email,
        'password': v.is_min_length(6)
    })

    user = db.query(User).filter_by(email=body['email']).first()

    if user is None:
        raise Error([error_item('email', 'Email doesn\'t exist.')])

    # validate password hash
    if bcrypt.checkpw(body['password'].encode('utf-8'), user.password.encode('utf-8')) == False:
        raise Error([error_item('password', 'Password doesn\'t match.')])

    # generate jwt for 1 week (for now)
    token = sign_token(user.id)

    return json_res(data={
        'id': user.id,
        'username': user.username,
        'picture': user.picture,
        'token': token,
    })


@userRoutes.get('/me')
def me_handler(db: Session):
    id = get_user_id()
    user = db.query(User).filter_by(id=id).first()

    return json_res(data={
        'id': user.id,
        'username': user.username,
        'picture': user.picture,
    })
