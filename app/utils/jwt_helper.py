import jwt
from datetime import datetime, timedelta
import os

SECRET = os.getenv('JWT_SECRET')


class JwtHelper:
    """ class JwtHelper provide an easy interface to interact with jwt
        package.
    """

    @staticmethod
    def sign(id: int):
        """ sign function allow to create a token for use by its `id`
            the create token currently stays `7 days`. 

            :param id: int value indicates `user id`
        """
        if type(id) != int:
            raise TypeError(f'Expected id of type int but found {type(id)}')

        return jwt.encode({
            'id': id,
            'date': datetime.now().isoformat(),
            "exp": datetime.utcnow() + timedelta(days=7)
        }, SECRET, algorithm='HS256')

    @staticmethod
    def verify(token: str):
        """ verify function verified a token from user
            incase the token is correct and valid it returns token's payload
            otherwise it throws and error means that validation failed

            :param token: the token which needed to be decoded and verified
        """
        return jwt.decode(token, SECRET, algorithms=['HS256'])
