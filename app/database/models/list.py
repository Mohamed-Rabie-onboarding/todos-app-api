from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from database.models.base import Base
from datetime import datetime


class Collection(Base):
    __tablename__ = 'collections'

    # table columns
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(Date, default=datetime.now())

    # relations
    user_id = Column(Integer, ForeignKey('users.id'))
    todos = relationship('Todo', cascade="all,delete")

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'todos': [todo.toDict() for todo in self.todos]
        }
