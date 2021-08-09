from typing import Union
from database.db import db_session as db

from database.models.base import IToOrm
from database.models.user import UserModel, UserOrm
from database.models.collection import CollectionModel, CollectionOrm
from database.models.todo import TodoModel, TodoOrm
from database.models.todo_item import TodoItemModel, TodoItemOrm


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


class TodoOrmHelper:
    @staticmethod
    def create_todo(todo: Union[TodoModel, TodoOrm]):
        return _OrmHelper.create_row(todo)

    @staticmethod
    def get_todo(id: int, user_id: int):
        return db.query(TodoOrm).filter_by(id=id, user_id=user_id).first()

    @staticmethod
    def update_todo(todo: TodoOrm, description: str):
        todo.description = description
        return db.commit()

    @staticmethod
    def remove_todo(id: int, user_id: int):
        q = db.query(TodoOrm).filter_by(id=id, user_id=user_id)
        return q.delete() == 1

    @staticmethod
    def get_user_todos(user_id: int):
        return db.query(TodoOrm).filter_by(user_id=user_id).all()

    @staticmethod
    def get_user_collection_todos(user_id: int, collection_id: int):
        return db.query(TodoOrm).filter_by(user_id=user_id, collection_id=collection_id).all()


class TodoItemOrmHelper:
    @staticmethod
    def create_todo_item(todo: Union[TodoItemModel, TodoItemOrm]):
        return _OrmHelper.create_row(todo)

    @staticmethod
    def get_todo_item(id: int, user_id: int):
        return db.query(TodoItemOrm).filter_by(id=id, user_id=user_id).first()

    @staticmethod
    def update_todo_item(item: TodoItemOrm, body=None, done=None):
        if body is not None:
            item.body = body

        if done is not None:
            item.done = done

        return db.commit()

    @staticmethod
    def remove_todo_item(id: int, user_id: int):
        q = db.query(TodoItemOrm).filter_by(id=id, user_id=user_id)
        return q.delete() == 1

    @staticmethod
    def get_user_items(user_id: int):
        return db.query(TodoItemOrm).filter_by(user_id=user_id).all()

    @staticmethod
    def get_user_todo_items(user_id: int, tood_id: int):
        return db.query(TodoItemOrm).filter_by(user_id=user_id, tood_id=tood_id).all()
