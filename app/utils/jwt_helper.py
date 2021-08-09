import jwt
from datetime import datetime, timedelta
import os

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
