from utils.validator_helper import create_errors
from bottle import request, response, abort
from utils.jwt_helper import JwtHelper


def required_auth(fn):
    def _get_user_id(*args, **kwargs):
        try:
            bearer: str = request.get_header('Authorization')
            token = bearer[len('bearer ')::]
            payload = JwtHelper.verify(token)
        except:
            abort(
                401,
                create_errors('Server', 'Unauthorized to make this request.')
            )

        # return the main router without try/catch
        # so it allow the error to flow for error routes
        return fn(payload.get('id'), *args, **kwargs)

    return _get_user_id


def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"

        if request.method != "OPTIONS":
            return fn(*args, **kwargs)

    return _enable_cors
