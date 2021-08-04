from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.models.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    # table columns
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    picture = Column(String, default='http://placehold.it/250x250')
    created_at = Column(Date, default=datetime.now())

    # relations
    lists = relationship('List', cascade="all,delete", backref="users")
