from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.models.base import Base
from datetime import datetime
from pydantic import BaseModel, validator, ValidationError
import bcrypt
from utils.validator_helper import ValidatorValueHelper


class UserOrm(Base):
    __tablename__ = 'users'

    # table columns
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    picture = Column(String(100), default='http://placehold.it/250x250')
    created_at = Column(Date, default=datetime.now())

    # relations
    lists = relationship('CollectionOrm', cascade="all,delete")
    todos = relationship('TodoOrm', cascade="all,delete")
    todos_items = relationship('TodoItemOrm', cascade="all,delete")

    def to_dict(self, token=None):
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
        hash_password = bcrypt.hashpw(
            self.password.encode('utf-8'),
            bcrypt.gensalt(12)
        )

        return UserOrm(
            username=self.username,
            email=self.email,
            password=hash_password
        )

    @validator('username')
    def username_validator(cls, value: str):
        return ValidatorValueHelper('Username', value).is_not_empty().has_min_length(3).has_max_length(20).get_value()

    @validator('email')
    def email_validator(cls, value: str):
        return ValidatorValueHelper('Email', value).is_not_empty().is_email_format().get_value()

    @validator('password')
    def password_validator(cls, value: str):
        return ValidatorValueHelper('Password', value).is_not_empty().has_min_length(6).has_max_length(80).get_value()

    @staticmethod
    def factory(body: dict):
        try:
            user = UserModel(**body)
            return (user.to_orm(), None)
        except ValidationError as e:
            return (None, ValidatorValueHelper.format_errors(e))
