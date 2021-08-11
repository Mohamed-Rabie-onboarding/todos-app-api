from sqlalchemy.orm.session import Session
from app.database.db import create_db_session
from unittest import TestCase
import os


class TestDB(TestCase):
    def test_create_db_session(self):
        with self.assertRaises(Exception):
            create_db_session()

        with self.assertRaises(Exception):
            create_db_session('invalid connection string')

        s = create_db_session(os.getenv('DB_URL'))
        self.assertEqual(type(s), Session)
