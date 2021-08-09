from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from database.models.base import Base
from datetime import datetime
from pydantic import BaseModel, validator, ValidationError
from utils.validator_helper import ValidatorValueHelper


class TodoItemOrm(Base):
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


class TodoItemModel(BaseModel):
    body: str

    def to_orm(self):
        return TodoItemOrm(
            body=self.body
        )

    @validator('body')
    def body_validator(cls, value: str):
        return ValidatorValueHelper('Body', value).is_not_empty().has_min_length(3).has_max_length(400).get_value()

    @staticmethod
    def factory(body: dict):
        try:
            todo_item = TodoItemOrm(**body)
            return todo_item.to_orm()
        except ValidationError as e:
            print(e.json())
            return e.json()
