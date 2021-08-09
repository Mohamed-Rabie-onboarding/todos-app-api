from utils.error import Error, error_item
from bottle import Bottle, request, response
from database.models.user import UserModel, UserOrm
import utils.validators as v
from utils.res import json_res
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from pymysql.err import IntegrityError as IE2
from utils.jwt import sign_token, get_user_id
from utils.decorators import inject_db, enable_cors
from utils.validator_helper import ValidatorValueHelper


userRoutes = Bottle()


@userRoutes.post('/')
@enable_cors
@inject_db
def register_handler(db: Session):
    user, errors = UserModel.factory(request.json)

    if errors is not None:
        response.status = 400
        return errors

    exist, error = ValidatorValueHelper.is_email_duplicated(
        db,
        UserOrm,
        user.email
    )

    if exist:
        response.status = 409
        return error

    db.add(user)
    db.commit()

    response.status = 201
    return {
        'message': 'User created!'
    }


# @userRoutes.post('/login')
# def login_handler(db: Session):
#     body = v.validate_body({
#         'email': v.is_email,
#         'password': v.is_min_length(6)
#     })

#     user = db.query(User).filter_by(email=body['email']).first()

#     if user is None:
#         raise Error([error_item('email', 'Email doesn\'t exist.')])

#     # validate password hash
#     if bcrypt.checkpw(body['password'].encode('utf-8'), user.password.encode('utf-8')) == False:
#         raise Error([error_item('password', 'Password doesn\'t match.')])

#     # generate jwt for 1 week (for now)
#     token = sign_token(user.id)

#     return json_res(data={
#         'id': user.id,
#         'username': user.username,
#         'picture': user.picture,
#         'token': token,
#     })


# @userRoutes.get('/me')
# def me_handler(db: Session):
#     id = get_user_id()
#     user = db.query(User).filter_by(id=id).first()

#     return json_res(data={
#         'id': user.id,
#         'username': user.username,
#         'picture': user.picture,
#     })
