from typing import Union
from database.db import db_session as db

from database.models.user import UserModel, UserOrm
from database.models.collection import CollectionModel, CollectionOrm
from database.models.todo import TodoModel, TodoOrm
from database.models.todo_item import TodoItemModel, TodoItemOrm


class UserOrmHelper:
    """ class UserOrmHelper
        provide an Orm interface to interact with `User` table
    """

    @staticmethod
    def create_user(user: Union[UserModel, UserOrm]):
        """ create_user creates new user in database

            :param user: An instance from `UserModel` or `UserOrm`
                         which has `to_orm` method.
        """
        db.add(user.to_orm())
        return db.commit()

    @staticmethod
    def is_user_exist(**kwargs):
        """ is_user_exist checks for a user existance by querying db with whatever
            passed on `kwargs`

            :param kwargs: Any unique identifier of the user `id` or `email`
        """
        q = db.query(UserOrm).filter_by(**kwargs)
        check = db.query(q.exists())
        return check.scalar()

    @staticmethod
    def get_user(**kwargs):
        """ get_user gets a user object from database if it exist
            otherwise it returns `None`

            :param kwargs: Any unique identifier of the user `id` or `email`
        """
        return db.query(UserOrm).filter_by(**kwargs).first()


class CollectionOrmHelper:
    """ class CollectionOrmHelper
        provide an Orm interface to interact with `Collection` table
    """
    @staticmethod
    def create_collection(collection: Union[CollectionModel, CollectionOrm]):
        """ create_collection creates new collection in database

            :param collection: An instance from `CollectionModel` or `CollectionOrm`
                         which has `to_orm` method.
        """
        db.add(collection.to_orm())
        return db.commit()

    @staticmethod
    def get_user_collections(user_id: int):
        """ get_user_collections gets all collections a specific user
            returns [] incase  there is no collections were found

            :param user_id: the user `id`
        """
        return db.query(CollectionOrm).filter_by(user_id=user_id).all()

    @staticmethod
    def get_collection(id: int, user_id: int):
        """ get_collection gets specific collection for a specific user
            returns `None` if collection not exists

            :param id: the collection `id`
            :param user_id: the user `id`
        """
        return db.query(CollectionOrm).filter_by(id=id, user_id=user_id).first()

    @staticmethod
    def remove_collection(id: int, user_id: int):
        """ remove_collection removes a specific collection for a specific user
            if the collection was found and remove its returns `True`
            if the collection was not found it return `False`

            :param id: the collection `id`
            :param user_id: the user `id`
        """
        q = db.query(CollectionOrm).filter_by(id=id, user_id=user_id)
        return q.delete() == 1

    @staticmethod
    def update_collection(collection: CollectionOrm, title: str):
        """ update_collection updates a specific collection for a specific user

            :param collection: the db_collection which needs update
            :param title: the new value for title for that collection
        """
        collection.title = title
        return db.commit()


class TodoOrmHelper:
    """ class TodoOrmHelper
        provide an Orm interface to interact with `Todo` table
    """
    @staticmethod
    def create_todo(todo: Union[TodoModel, TodoOrm]):
        """ create_todo creates new todo in database

            :param todo: An instance from `TodoModel` or `TodoOrm`
                         which has `to_orm` method.
        """
        db.add(todo.to_orm())
        return db.commit()

    @staticmethod
    def get_todo(id: int, user_id: int):
        """ get_todo gets specific todo for a specific user
            returns `None` if todo not exists

            :param id: the todo `id`
            :param user_id: the user `id`
        """
        return db.query(TodoOrm).filter_by(id=id, user_id=user_id).first()

    @staticmethod
    def update_todo(todo: TodoOrm, description: str):
        """ update_todo updates a specific todo for a specific user

            :param todo: the db_todo which needs update
            :param description: the new value for description for that todo
        """
        todo.description = description
        return db.commit()

    @staticmethod
    def remove_todo(id: int, user_id: int):
        """ remove_todo removes a specific todo for a specific user
            if the todo was found and remove its returns `True`
            if the todo was not found it return `False`

            :param id: the todo `id`
            :param user_id: the user `id`
        """
        q = db.query(TodoOrm).filter_by(id=id, user_id=user_id)
        return q.delete() == 1

    @staticmethod
    def get_user_todos(user_id: int):
        """ get_user_todos gets all todos for a specific user
            returns [] incase  there is no todos were found

            :param user_id: the user `id`
        """
        return db.query(TodoOrm).filter_by(user_id=user_id).all()

    @staticmethod
    def get_user_collection_todos(user_id: int, collection_id: int):
        """ get_user_collection_todos gets all todos 
            for a specific collection for a specific user
            returns [] incase  there is no todos were found

            :param user_id: the user `id`
        """
        return db.query(TodoOrm).filter_by(user_id=user_id, collection_id=collection_id).all()


class TodoItemOrmHelper:
    """ class TodoItemOrmHelper
        provide an Orm interface to interact with `TodoItem` table
    """
    @staticmethod
    def create_todo_item(todoItem: Union[TodoItemModel, TodoItemOrm]):
        """ create_todo_item creates new todoItem in database

            :param todoItem: An instance from `TodoItemModel` or `TodoItemOrm`
                         which has `to_orm` method.
        """
        db.add(todoItem.to_orm())
        return db.commit()

    @staticmethod
    def get_todo_item(id: int, user_id: int):
        """ get_todo_item gets a specific todoItem for a specific user
            if todoItem not found it returns `None`

            :param id: the todoItem `id`
            :param user_id: the user `id`
        """
        return db.query(TodoItemOrm).filter_by(id=id, user_id=user_id).first()

    @staticmethod
    def update_todo_item(item: TodoItemOrm, body=None, done=None):
        """ update_todo_item updates a specific todo for a specific user

            :param item: the db_todoItem which needs update
            :param body: the new value for body for that item
            :param done: the new value for done for that item
        """
        if body is not None:
            item.body = body

        if done is not None:
            item.done = done

        return db.commit()

    @staticmethod
    def remove_todo_item(id: int, user_id: int):
        """ remove_todo_item removes a specific todoItem for a specific user
            if the todoItem was found and remove its returns `True`
            if the todoItem was not found it return `False`

            :param id: the todoItem `id`
            :param user_id: the user `id`
        """
        q = db.query(TodoItemOrm).filter_by(id=id, user_id=user_id)
        return q.delete() == 1

    @staticmethod
    def get_user_items(user_id: int):
        """ get_user_items gets todoItems for a specific user
            returns [] if no todoItem were found

            :param user_id: the user `id`
        """
        return db.query(TodoItemOrm).filter_by(user_id=user_id).all()

    @staticmethod
    def get_user_todo_items(user_id: int, tood_id: int):
        """ get_user_todo_items gets todoItems for a specific todo for a specific user
            returns [] if no todoItem were found

            :param user_id: the user `id`
            :param todo_id: the todo `id`
        """
        return db.query(TodoItemOrm).filter_by(user_id=user_id, tood_id=tood_id).all()
