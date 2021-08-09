from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.models.base import Base
from datetime import datetime
from pydantic import BaseModel, validator, ValidationError, validate_email
from utils.error import is_not_empty
import bcrypt


class UserOrm(Base):
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

    def dict(self, token=None):
        user = {
            'id': self.id,
            'username': self.username,
            'picture': self.picture,
        }
        if token is not None:
            user['token'] = token
        return user


class UserModel(BaseModel):
    username: str
    email: str
    password: str

    def to_orm(self):
        return UserOrm(
            username=self.username,
            email=self.email,
            password=bcrypt.hashpw(
                self.password.encode('utf-8'),
                bcrypt.gensalt(12)
            )
        )

    @validator('username')
    def username_validator(cls, value: str):
        value = is_not_empty(value, 'Username')
        if len(value) < 3:
            raise ValueError('Username must be more than 2 chars.')
        return value

    @validator('email')
    def email_validator(cls, value: str):
        value = is_not_empty(value, 'Email')
        if not validate_email(value):
            raise ValueError('Email is not correct.')
        return value

    @validator('password')
    def password_validator(cls, value: str):
        value = is_not_empty(value, 'Password')
        if len(value) < 6:
            raise ValueError('Password min length is 6 chars.')
        return value

    @staticmethod
    def factory(body: dict):
        try:
            user = UserModel(**body)
            return user.to_orm()
        except ValidationError as e:
            print(e.json())
            return e.json()
