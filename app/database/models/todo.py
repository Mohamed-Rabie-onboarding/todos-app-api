from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
from datetime import datetime


class Todo(Base):
    __tablename__ = 'todos'

    # table columns
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=True)
    created_at = Column(Date, default=datetime.now())

    # relations
    items = relationship('TodoItem', cascade="all,delete", backref="todos")
    list_id = Column(Integer, ForeignKey('List.id'))


class TodoItem(Base):
    __tablename__ = 'items'

    # table columns
    id = Column(Integer, primary_key=True)
    body = Column(String, nullable=False)
    created_at = Column(Date, default=datetime.now())

    # relations
    todo_id = Column(Integer, ForeignKey('Todo.id'))
