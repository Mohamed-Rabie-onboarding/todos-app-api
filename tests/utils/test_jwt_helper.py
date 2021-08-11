from unittest import TestCase
from app.utils.jwt_helper import JwtHelper


class TestJwtHelper(TestCase):

    def test_sign(self):
        token = JwtHelper.sign(1)
        self.assertEqual(type(token), str)

        with self.assertRaises(Exception):
            JwtHelper.sign()
            JwtHelper.sign('1')

    def test_verify(self):
        token = JwtHelper.sign(1)
        payload = JwtHelper.verify(token)
        self.assertEqual(payload['id'], 1)

        with self.assertRaises(Exception):
            JwtHelper.verify()
            JwtHelper.verify('wrong token')
