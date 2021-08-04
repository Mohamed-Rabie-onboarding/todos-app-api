from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.models.base import Base
from datetime import datetime


class List(Base):
    __tablename__ = 'lists'

    # table columns
    id = Column(Integer, primary_key=True)
    created_at = Column(Date, default=datetime.now())

    # relations
    user_id = Column(Integer, ForeignKey('users.id'))
    todos = relationship('Todo', cascade="all,delete")
