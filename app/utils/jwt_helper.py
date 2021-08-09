import jwt
from datetime import datetime, timedelta
import os
from utils.error import Error, system_error_item
# from bottle import request

SECRET = os.getenv('JWT_SECRET')


class JwtHelper:

    @staticmethod
    def sign(id: int):
        return jwt.encode({
            'id': id,
            'date': datetime.now().isoformat(),
            "exp": datetime.utcnow() + timedelta(days=7)
        }, SECRET, algorithm='HS256')

    @staticmethod
    def verify(token: str):
        return jwt.decode(token, SECRET, algorithms=['HS256'])


# def get_user_id():
#     try:
#         bearer: str = request.get_header('Authorization')
#         token = bearer[len('bearer ')::]
#         payload = verify_token(token)
#         return payload.get('id')
#     except Exception:
#         raise Error([system_error_item('Please login again.')])
