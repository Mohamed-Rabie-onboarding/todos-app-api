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
    password = Column(String(50), nullable=False)
    picture = Column(String(100), default='http://placehold.it/250x250')
    created_at = Column(Date, default=datetime.now())

    # relations
    lists = relationship('List', cascade="all,delete")
