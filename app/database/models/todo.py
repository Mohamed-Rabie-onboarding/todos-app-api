from sqlalchemy import Column, Integer, String, Date, ForeignKey
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
    list_id = Column(Integer, ForeignKey('lists.id'))
    items = relationship('TodoItem', cascade="all,delete")


class TodoItem(Base):
    __tablename__ = 'items'

    # table columns
    id = Column(Integer, primary_key=True)
    body = Column(String(500), nullable=False)
    created_at = Column(Date, default=datetime.now())

    # relations
    todo_id = Column(Integer, ForeignKey('todos.id'))
