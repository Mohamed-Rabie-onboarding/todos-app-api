from bottle import abort
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database.models.base import Base, IToOrm
from datetime import datetime
from pydantic import BaseModel, validator, ValidationError
import bcrypt
from utils.validator_helper import ValidatorHelper


class UserOrm(Base, IToOrm):
    """ class UserOrm
        A class representation of User model in database
    """
    __tablename__ = 'users'

    # table columns
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    picture = Column(String(100), default='http://placehold.it/250x250')
    created_at = Column(Date, default=datetime.now())

    # relations
    collections = relationship('CollectionOrm', cascade="all,delete")
    todos = relationship('TodoOrm', cascade="all,delete")
    todos_items = relationship('TodoItemOrm', cascade="all,delete")

    def to_dict(self, token=None):
        """ to_dict turns the only public fields of a user model into a dict
            so it can be used as a returned value from routes
        """
        user = {
            'id': self.id,
            'username': self.username,
            'picture': self.picture,
        }
        if token is not None:
            user['token'] = token
        return user


class UserModel(BaseModel):
    """ class UserModel
        Initialize this class cause a validation check py `pydantic` package
    """
    # metadata
    include_username: bool

    username: str
    email: str
    password: str

    def to_orm(self, **kwargs):
        """ to_orm turns `UserModel` into `UserOrm`
            so it can be used with database
            as this class won't be used unless u're creating new user
            so it hash password while converting to `UserOrm`
        """
        hash_password = bcrypt.hashpw(
            self.password.encode('utf-8'),
            bcrypt.gensalt(12),
        )

        return UserOrm(
            username=self.username if self.include_username else None,
            email=self.email,
            password=hash_password,
            **kwargs
        )

    def password_matched(self, hash: str):
        """ password_matched checks if the password and hashed value
            matches eachother
        """
        return bcrypt.checkpw(self.password.encode('utf-8'), hash.encode('utf-8'))

    @validator('username')
    def username_validator(cls, value: str):
        return ValidatorHelper('Username', value).is_not_empty().has_min_length(3).has_max_length(20).get_value()

    @validator('email')
    def email_validator(cls, value: str):
        return ValidatorHelper('Email', value).is_not_empty().is_email_format().get_value()

    @validator('password')
    def password_validator(cls, value: str):
        return ValidatorHelper('Password', value).is_not_empty().has_min_length(6).has_max_length(80).get_value()

    @staticmethod
    def factory(body: dict, username=True):
        """ factory create a UserModel and handle error
            if validation didn't pass
        """
        try:
            body = body if (body is not None) else {}

            # temp solution
            body['include_username'] = username
            if not username:
                body['username'] = 'xxxxxxxxx'

            return UserModel(**body)
        except ValidationError as e:
            abort(400, ValidatorHelper.format_errors(e))
