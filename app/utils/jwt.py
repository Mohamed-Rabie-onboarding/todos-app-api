import jwt
from datetime import datetime, timedelta
import os
from utils.error import Error, system_error_item
from bottle import request

SECRET = os.getenv('JWT_SECRET')


def sign_token(id: int):
    message = {
        'id': id,
        'date': datetime.now().isoformat(),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(message, SECRET, algorithm='HS256')
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        return payload
    except Exception:
        raise Error([system_error_item('Please login again.')])


def get_user_id():
    try:
        bearer: str = request.get_header('Authorization')
        token = bearer[len('bearer ')::]
        payload = verify_token(token)
        return payload.get('id')
    except Exception:
        raise Error([system_error_item('Please login again.')])
