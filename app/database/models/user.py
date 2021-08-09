from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.models.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    # table columns
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    picture = Column(String(100), default='http://placehold.it/250x250')
    created_at = Column(Date, default=datetime.now())

    # relations
    lists = relationship('Collection', cascade="all,delete")
    todos = relationship('Todo', cascade="all,delete")
    todos_items = relationship('TodoItem', cascade="all,delete")

    def toDict(self, token):
        user = {
            'id': self.id,
            'username': self.username,
            'picture': self.picture,
        }

        if token is not None:
            user['token'] = token

        return user
