from typing import Union
from database.db import db_session as db

from database.models.base import IToOrm
from database.models.user import UserModel, UserOrm
from database.models.collection import CollectionModel, CollectionOrm


class _OrmHelper:
    @staticmethod
    def create_row(row: IToOrm):
        db.add(row.to_orm())
        return db.commit()


class UserOrmHelper:
    @staticmethod
    def create_user(user: Union[UserModel, UserOrm]):
        return _OrmHelper.create_row(user)

    @staticmethod
    def is_user_exist(**kwargs):
        q = db.query(UserOrm).filter_by(**kwargs)
        check = db.query(q.exists())
        return check.scalar()

    @staticmethod
    def get_user(**kwargs):
        return db.query(UserOrm).filter_by(**kwargs).first()


class CollectionOrmHelper:
    @staticmethod
    def create_collection(collection: Union[CollectionModel, CollectionOrm]):
        return _OrmHelper.create_row(collection)

    @staticmethod
    def get_user_collections(user_id: int):
        return db.query(CollectionOrm).filter_by(user_id=user_id).all()

    @staticmethod
    def get_collection(id: int, user_id: int):
        return db.query(CollectionOrm).filter_by(id=id, user_id=user_id).first()

    @staticmethod
    def remove_collection(id: int, user_id: int):
        q = db.query(CollectionOrm).filter_by(id=id, user_id=user_id)
        return q.delete() == 1

    @staticmethod
    def update_collection(collection: CollectionOrm, title: str):
        collection.title = title
        return db.commit()
