import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from database.models.base import Base
from sqlalchemy.orm import Session

# import models to be defined
from database.models.list import Collection
from database.models.user import UserOrm
from database.models.todo import Todo, TodoItem


def create_db_session(uri: str):
    engine = create_engine(uri)

    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(
            engine,
            tables=[
                UserOrm.__table__,
                Collection.__table__,
                Todo.__table__,
                TodoItem.__table__,
            ],
        )

    return Session(engine)


__session__: Session = None


def get_db_session():
    global __session__

    if __session__ is None:
        __session__ = create_db_session(os.getenv('DB_URL'))

    return __session__
