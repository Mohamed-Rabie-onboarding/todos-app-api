from unittest import TestCase
from app.utils.decorators import required_auth, enable_cors
from app.utils.jwt_helper import JwtHelper
from bottle import Bottle, response
from webtest import TestApp


class TestDecorators(TestCase):

    def test_required_auth(self):
        app = Bottle()
        app_test = TestApp(app)

        @app.get('/')
        @required_auth
        def required_auth_next(user_id: int):
            self.assertEqual(user_id, 1)
            return {'ok': True}

        @app.error(401)
        def error_401_handler(err):
            response.status = 401
            response.set_header('content-type', 'application/json')
            return err.body

        # fail case
        res1 = app_test.get('/', expect_errors=True)
        self.assertEqual(res1.status_int, 401)
        self.assertDictEqual(res1.json, dict(
            errors=[
                dict(
                    field="Server",
                    message='Unauthorized to make this request.'
                )
            ]
        ))

        # success case
        t = f"bearer {JwtHelper.sign(1)}"
        res2 = app_test.get('/', headers=dict(Authorization=t))
        self.assertEqual(res2.status_int, 200)
        self.assertDictEqual(res2.json, dict(ok=True))

    def test_enable_cors(self):
        app = Bottle()
        app_test = TestApp(app)

        @app.get('/')
        @enable_cors
        def enable_cors_next():
            return {'ok': True}

        res = app_test.get('/')
        headers = res.headers

        self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
        self.assertEqual(
            headers['Access-Control-Allow-Methods'],
            'GET, POST, PUT, OPTIONS, DELETE'
        )
        self.assertEqual(
            headers['Access-Control-Allow-Headers'],
            "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"
        )
