from bottle import request, response
from database.db import get_db_session


def inject_db(fn):
    def _inject_db(*args, **kwargs):
        print('injected db')
        return fn(get_db_session(), *args, **kwargs)

    return _inject_db


def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        print('enabled cors')
        # set CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS, DELETE"
        response.headers[
            "Access-Control-Allow-Headers"
        ] = "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"

        if request.method != "OPTIONS":
            return fn(*args, **kwargs)

    return _enable_cors
