from typing import Optional
from bottle import abort
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from database.models.base import Base, IToOrm
from datetime import datetime
from pydantic import BaseModel, validator, ValidationError
from utils.validator_helper import ValidatorHelper


class TodoItemOrm(Base, IToOrm):
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
    done: Optional[bool]

    def to_orm(self, **kwargs):
        return TodoItemOrm(
            body=self.body,
            **kwargs
        )

    @validator('body')
    def body_validator(cls, value: str):
        return ValidatorHelper('Body', value).is_not_empty().has_min_length(3).has_max_length(400).get_value()

    @validator('done')
    def done_validator(cls, value: bool):
        return ValidatorHelper('Done', value).is_bool().get_value()

    @staticmethod
    def factory(body: dict, can_ignore_body=False):
        try:
            body = body if (body is not None) else {}

            # temp solution
            if can_ignore_body and 'body' not in body:
                body['body'] = 'xxxxx'

            return TodoItemModel(**body)
        except ValidationError as e:
            abort(400, ValidatorHelper.format_errors(e))
