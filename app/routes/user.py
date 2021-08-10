from bottle import Bottle, request, response
from database.models.user import UserModel
from utils.jwt_helper import JwtHelper
from utils.decorators import enable_cors, required_auth
from utils.validator_helper import ValidatorHelper
from utils.orm_helper import UserOrmHelper
from routes.error import errorRoutes


userRoutes = Bottle()


@userRoutes.post('/')
@enable_cors
def create_user_handler():
    user, errors = UserModel.factory(request.json)

    if errors is not None:
        response.status = 400
        return errors

    if UserOrmHelper.is_user_exist(email=user.email):
        response.status = 409
        return ValidatorHelper.create_error('email', 'Email is duplicated.')

    UserOrmHelper.create_user(user)

    response.status = 201


@userRoutes.post('/authenticate')
@enable_cors
def authenticate_user_handler():
    user, errors = UserModel.factory(request.json, username=False)

    if errors is not None:
        response.status = 400
        return errors

    db_user = UserOrmHelper.get_user(email=user.email)

    if db_user is None or not user.password_matched(db_user.password):
        response.status = 401
        return ValidatorHelper.create_error('email', 'Email and password do not match.')

    response.status = 201
    return db_user.to_dict(
        JwtHelper.sign(db_user.id)
    )


@userRoutes.get('/')
@enable_cors
@required_auth
def get_current_user_handler(user_id: int):
    db_user = UserOrmHelper.get_user(id=user_id)

    response.status = 200
    return db_user.to_dict()
