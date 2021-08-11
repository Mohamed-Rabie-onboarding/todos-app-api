from app.routes.user import userRoutes
from unittest import TestCase
from webtest import TestApp
from json import dumps


class TestUserRoutes(TestCase):
    app = TestApp(userRoutes)

    def test_create_user_handler_400_1(self):
        res = self.app.post('/', expect_errors=True)
        self.assertEqual(res.status_int, 400)
        self.assertDictEqual(
            res.json,
            dict(
                errors=[
                    dict(field='username', message='Username is required.'),
                    dict(field='email', message='Email is required.'),
                    dict(field='password', message='Password is required.')
                ]
            )
        )

    def test_create_user_handler_400_2(self):
        data = dict(username="M", email="x", password="x")
        res = self.app.post(
            '/',
            expect_errors=True,
            params=dumps(data),
            content_type='application/json'
        )
        self.assertEqual(res.status_int, 400)
        self.assertDictEqual(
            res.json,
            dict(
                errors=[
                    dict(
                        field='username',
                        message='Username must be more than 2 chars.'
                    ),
                    dict(
                        field='email',
                        message='Email is not correct.'
                    ),
                    dict(
                        field='password',
                        message='Password must be more than 5 chars.'
                    )
                ]
            )
        )
