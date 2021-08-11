from bottle import request, response, abort
from utils.validator_helper import create_errors
from utils.jwt_helper import JwtHelper


def required_auth(fn):
    """ Using required_auth with any bottle router adding extra check 
        and the current login user before enter that router
        the checking done by extracting `Authorization` header
        and parsing it to match format `bearer $token`
        after getting token from parsing it trys to verify it
        if verification success the payload returns otherwise 
        it throws and Exception with code (401)
    """
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
    """ Using enable_cors with any bottle router enables cors for that router
        by enabling cors this router becomes accessable from front end
        whenever the request method isn't `OPTIONS` the router itself runs.
    """
    def _enable_cors(*args, **kwargs):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"

        if request.method != "OPTIONS":
            return fn(*args, **kwargs)

    return _enable_cors
