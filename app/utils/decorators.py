from utils.validator_helper import ValidatorHelper
from bottle import request, response
from database.db import db_session
from utils.jwt_helper import JwtHelper


def inject_db(fn):
    def _inject_db(*args, **kwargs):
        return fn(db_session, *args, **kwargs)

    return _inject_db


def required_auth(fn):
    def _get_user_id(*args, **kwargs):
        try:
            bearer: str = request.get_header('Authorization')
            token = bearer[len('bearer ')::]
            payload = JwtHelper.verify(token)
            return fn(payload.get('id'), *args, **kwargs)
        except Exception as e:
            response.status = 401
            return ValidatorHelper.create_error(
                'Server',
                'Unauthorized to make this request.'
            )

    return _get_user_id


def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"

        if request.method != "OPTIONS":
            return fn(*args, **kwargs)

    return _enable_cors
