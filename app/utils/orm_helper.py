from typing import Union
from database.models.user import UserModel, UserOrm
from database.db import db_session as db


class UserOrmHelper:
    @staticmethod
    def create_user(user: Union[UserModel, UserOrm]):
        db.add(user.to_orm())
        return db.commit()

    @staticmethod
    def is_user_exist(**kwargs):
        q = db.query(UserOrm).filter_by(**kwargs)
        check = db.query(q.exists())
        return check.scalar()

    @staticmethod
    def get_user(**kwargs):
        return db.query(UserOrm).filter_by(**kwargs).first()
