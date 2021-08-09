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
from utils.validator_helper import ValidatorHelper
from utils.orm_helper import OrmHelper


userRoutes = Bottle()


@userRoutes.post('/')
@enable_cors
@inject_db
def create_user_handler(db: Session):
    user, errors = UserModel.factory(request.json)

    if errors is not None:
        response.status = 400
        return errors

    if OrmHelper.is_user_exist(db, email=user.email):
        response.status = 409
        return ValidatorHelper.duplicated_email_error()

    OrmHelper.create_user(user)

    response.status = 201
    return {
        'message': 'User created!'
    }


@userRoutes.post('/authenticate')
@enable_cors
@inject_db
def authenticate_user_handler(db: Session):
    user, errors = UserModel.factory(request.json)

    if errors is not None:
        response.status = 400
        return errors

    # user = db.query(User).filter_by(email=body['email']).first()

    # if user is None:
    #     raise Error([error_item('email', 'Email doesn\'t exist.')])

    # # validate password hash
    # if bcrypt.checkpw(body['password'].encode('utf-8'), user.password.encode('utf-8')) == False:
    #     raise Error([error_item('password', 'Password doesn\'t match.')])

    # # generate jwt for 1 week (for now)
    # token = sign_token(user.id)

    # return json_res(data={
    #     'id': user.id,
    #     'username': user.username,
    #     'picture': user.picture,
    #     'token': token,
    # })

    # @userRoutes.get('/me')
    # def me_handler(db: Session):
    #     id = get_user_id()
    #     user = db.query(User).filter_by(id=id).first()

    #     return json_res(data={
    #         'id': user.id,
    #         'username': user.username,
    #         'picture': user.picture,
    #     })
