from app.routes.user import userRoutes
from unittest import TestCase
from webtest import TestApp
from tests.test_base import TestHelpers


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
        res = self.app.post_json(
            '/',
            params=data,
            expect_errors=True,
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

    def test_create_user_handler_200_409(self):
        email = f"{TestHelpers.random_string()}@duo.com"
        data = dict(username="Jhon", email=email, password="123465")

        res200 = self.app.post_json('/', params=data)
        self.assertEqual(res200.status_int, 201)
        self.assertEqual(res200.body.decode('utf-8'), '')

        res409 = self.app.post_json('/', params=data, expect_errors=True)
        self.assertEqual(res409.status_int, 409)
        self.assertDictEqual(
            res409.json,
            dict(
                errors=[
                    dict(
                        field="email",
                        message="Email is duplicated."
                    )
                ]
            )
        )
