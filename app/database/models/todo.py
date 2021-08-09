from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.models.base import Base, IToOrm
from datetime import datetime
from pydantic import BaseModel, validator, ValidationError
from utils.validator_helper import ValidatorHelper


class TodoOrm(Base, IToOrm):
    __tablename__ = 'todos'

    # table columns
    id = Column(Integer, primary_key=True)
    description = Column(String(400), nullable=True)
    created_at = Column(Date, default=datetime.now())

    # relations
    user_id = Column(Integer, ForeignKey('users.id'))
    collection_id = Column(Integer, ForeignKey('collections.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'list_id': self.list_id,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat()
        }


class TodoModel(BaseModel):
    description: str

    def to_orm(self, **kwargs):
        return TodoOrm(
            description=self.description,
            **kwargs
        )

    @validator('description')
    def description_validator(cls, value: str):
        return ValidatorHelper('Description', value).is_not_empty().has_min_length(3).has_max_length(400).get_value()

    @staticmethod
    def factory(body: dict):
        try:
            return (TodoModel(**body), None)
        except ValidationError as e:
            return (None, ValidatorHelper.format_errors(e))
