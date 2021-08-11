from bottle import Bottle, request, response, abort
from app.database.models.user import UserModel
from app.utils.jwt_helper import JwtHelper
from app.utils.decorators import enable_cors, required_auth
from app.utils.validator_helper import create_errors
from app.utils.orm_helper import UserOrmHelper
from app.routes.error import error_handler


userRoutes = Bottle()
userRoutes.error_handler = error_handler


@userRoutes.post('/')
@enable_cors
def create_user_handler():
    """ create_user_handler
        takes in `body` includes username, email and password
        responses:
            - 201: User created & no content to create.
            - 400: invalid data.
            - 409: Email is duplicated.
    """
    user = UserModel.factory(request.json)

    if UserOrmHelper.is_user_exist(email=user.email):
        abort(409, create_errors('email', 'Email is duplicated.'))

    UserOrmHelper.create_user(user)
    response.status = 201


@userRoutes.post('/authenticate')
@enable_cors
def authenticate_user_handler():
    """ authenticate_user_handler
        takes in `body` includes email and password
        responses:
            - 201: User created & returns user with created token.
            - 400: invalid data.
            - 401: Email and password do not match.
    """
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
    """ get_current_user_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 200: User found and returned.
            - 401: Unauthorized to make this request.
    """
    db_user = UserOrmHelper.get_user(id=user_id)

    response.status = 200
    return db_user.to_dict()
