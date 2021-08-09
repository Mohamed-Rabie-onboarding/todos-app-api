from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database.models.base import Base
from datetime import datetime


class Todo(Base):
    __tablename__ = 'todos'

    # table columns
    id = Column(Integer, primary_key=True)
    description = Column(String(400), nullable=True)
    created_at = Column(Date, default=datetime.now())

    # relations
    user_id = Column(Integer, ForeignKey('users.id'))
    list_id = Column(Integer, ForeignKey('collections.id'))
    items = relationship('TodoItem', cascade="all,delete")

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'list_id': self.list_id,
            'items': [(item) for item in self.items],
            'created_at': self.created_at.isoformat()
        }


class TodoItem(Base):
    __tablename__ = 'items'

    # table columns
    id = Column(Integer, primary_key=True)
    body = Column(String(500), nullable=False)
    done = Column(Boolean, default=False)
    created_at = Column(Date, default=datetime.now())

    # relations
    user_id = Column(Integer, ForeignKey('users.id'))
    todo_id = Column(Integer, ForeignKey('todos.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'done': self.done,
            'todo_id': self.todo_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }
