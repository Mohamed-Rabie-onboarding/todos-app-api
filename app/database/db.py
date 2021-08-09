import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from database.models.base import Base
from sqlalchemy.orm import Session

# import models to be defined
from database.models.collection import CollectionOrm
from database.models.user import UserOrm
from database.models.todo import TodoOrm
from database.models.todo_item import TodoItemOrm


def create_db_session(uri: str):
    engine = create_engine(uri)

    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(
            engine,
            tables=[
                UserOrm.__table__,
                CollectionOrm.__table__,
                TodoOrm.__table__,
                TodoItemOrm.__table__,
            ],
        )

    return Session(engine)


db_session = create_db_session(os.getenv('DB_URL'))
