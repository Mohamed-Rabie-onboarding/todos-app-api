import os
import bottle_sqlalchemy
from sqlalchemy import create_engine


def create_db_plugin():
    engine = create_engine(os.environ.get('DB_URL'))
    plugin = bottle_sqlalchemy.SQLAlchemyPlugin(engine, keyword='db')
    return plugin
