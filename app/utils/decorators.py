from bottle import request, response
from database.db import db_session


def inject_db(fn):
    def _inject_db(*args, **kwargs):
        return fn(db_session, *args, **kwargs)

    return _inject_db


def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"

        if request.method != "OPTIONS":
            return fn(*args, **kwargs)

    return _enable_cors
