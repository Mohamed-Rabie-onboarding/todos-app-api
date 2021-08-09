import os
import bottle_sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from database.models.base import Base

# import models to be defined
from database.models.list import Collection
from database.models.user import User
from database.models.todo import Todo, TodoItem


def create_db_plugin(uri: str):
    engine = create_engine(uri)

    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(
            engine,
            tables=[
                User.__table__,
                Collection.__table__,
                Todo.__table__,
                TodoItem.__table__,
            ],
        )

    plugin = bottle_sqlalchemy.SQLAlchemyPlugin(engine, keyword='db')
    return plugin
