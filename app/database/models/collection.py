from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from database.models.base import Base, IToOrm
from datetime import datetime
from pydantic import BaseModel, validator, ValidationError
from utils.validator_helper import ValidatorHelper


class CollectionOrm(Base, IToOrm):
    __tablename__ = 'collections'

    # table columns
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    created_at = Column(Date, default=datetime.now())

    # relations
    user_id = Column(Integer, ForeignKey('users.id'))
    todos = relationship('TodoOrm', cascade="all,delete")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'user_id': self.user_id,
            'todos': [todo.to_dict() for todo in self.todos],
            'created_at': self.created_at.isoformat()
        }


class CollectionModel(BaseModel):
    title: str

    def to_orm(self, **kwargs):
        return CollectionOrm(
            title=self.title,
            **kwargs
        )

    @validator('title')
    def title_validator(cls, value: str):
        return ValidatorHelper('Title', value).is_not_empty().has_min_length(3).has_max_length(100).get_value()

    @staticmethod
    def factory(body: dict):
        try:
            return (CollectionModel(**body), None)
        except ValidationError as e:
            return (None, ValidatorHelper.format_errors(e))
