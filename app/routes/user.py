from bottle import Bottle, request, response, abort
from database.models.user import UserModel
from utils.jwt_helper import JwtHelper
from utils.decorators import enable_cors, required_auth
from utils.validator_helper import create_errors
from utils.orm_helper import UserOrmHelper
from routes.error import error_handler


userRoutes = Bottle()
userRoutes.error_handler = error_handler


@userRoutes.post('/')
@enable_cors
def create_user_handler():
    user = UserModel.factory(request.json)

    if UserOrmHelper.is_user_exist(email=user.email):
        abort(409, create_errors('email', 'Email is duplicated.'))

    UserOrmHelper.create_user(user)
    response.status = 201


@userRoutes.post('/authenticate')
@enable_cors
def authenticate_user_handler():
    user = UserModel.factory(request.json, username=False)

    db_user = UserOrmHelper.get_user(email=user.email)

    if db_user is None or not user.password_matched(db_user.password):
        abort(401, create_errors('email', 'Email and password do not match.'))

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
