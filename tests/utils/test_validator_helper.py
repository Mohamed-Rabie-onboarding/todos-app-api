from unittest import TestCase
from bottle import HTTPError
import app.utils.validator_helper as h
from pydantic import BaseModel, validator, ValidationError


class TestValidatorHelper(TestCase):

    def test_create_error(self):
        self.assertDictEqual(
            h._create_error('x', 'xyz'),
            dict(field='x', message='xyz')
        )

    def test_create_errors(self):
        self.assertDictEqual(
            h.create_errors('x', 'xyz'),
            dict(errors=[dict(field='x', message='xyz')])
        )

    def test_not_found_error(self):
        with self.assertRaises(HTTPError):
            h.not_found_error('x')

    def test_error_if_not_found(self):
        self.assertEqual(
            h.error_if_not_found(True, 'x'),
            None
        )

        with self.assertRaises(HTTPError):
            h.error_if_not_found(False, 'x')

        with self.assertRaises(HTTPError):
            h.error_if_not_found(None, 'x')

    def test_validator_helper(self):
        with self.assertRaises(TypeError):
            h.ValidatorHelper()

        with self.assertRaises(ValueError):
            h.ValidatorHelper('   ', 'asd')

        with self.assertRaises(TypeError):
            h.ValidatorHelper(None, 'asd')

    def test_is_not_empty(self):
        instance = h.ValidatorHelper('f', 'x').is_not_empty()
        self.assertEqual(instance.is_not_empty(), instance)

        with self.assertRaises(ValueError):
            h.ValidatorHelper('x', '     ').is_not_empty()

        with self.assertRaises(ValueError):
            h.ValidatorHelper('x', '').is_not_empty()

    def test_is_bool(self):
        instance1 = h.ValidatorHelper('f', True).is_bool()
        self.assertEqual(instance1.is_bool(), instance1)

        instance2 = h.ValidatorHelper('f', False).is_bool()
        self.assertEqual(instance2.is_bool(), instance2)

        with self.assertRaises(ValueError):
            h.ValidatorHelper('x', '').is_bool()

    def test_has_min_length(self):
        instance = h.ValidatorHelper('f', 'sad')
        self.assertEqual(instance.has_min_length(2), instance)

        with self.assertRaises(ValueError):
            h.ValidatorHelper('x', '    ').has_min_length(2)

    def test_has_max_length(self):
        instance = h.ValidatorHelper('f', 'a' * 10)
        self.assertEqual(instance.has_max_length(10), instance)

        with self.assertRaises(ValueError):
            h.ValidatorHelper('x', 'a' * 11).has_max_length(10)

    def test_is_email_format(self):
        instance = h.ValidatorHelper('f', 'test@test.com')
        self.assertEqual(instance.is_email_format(), instance)

        with self.assertRaises(ValueError):
            h.ValidatorHelper('x', 'wrong-mail').is_email_format()

    def test_get_value(self):
        self.assertEqual(h.ValidatorHelper('f', 'x').get_value(), 'x')

    def test_format_errors(self):
        class FakeModel(BaseModel):
            fake: str

            @validator('fake')
            def fake_validator(cls, value):
                h.ValidatorHelper('fake', value).is_not_empty().get_value()

        try:
            FakeModel(fake="")
        except ValidationError as e:
            errors = e

        self.assertDictEqual(
            h.ValidatorHelper.format_errors(errors),
            dict(
                errors=[
                    dict(
                        field='fake',
                        message='fake is required.'
                    )
                ]
            )
        )
