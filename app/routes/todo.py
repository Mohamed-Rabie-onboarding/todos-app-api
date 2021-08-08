from bottle import Bottle, debug
from sqlalchemy.orm.session import Session
from utils.jwt import get_user_id
from utils.res import json_res
import utils.validators as v
from database.models.todo import Todo, TodoItem
from utils.error import Error, system_error_item


def extract_todo(todo: Todo):
    return {
        'id': todo.id,
        'description': todo.description,
        'list_id': todo.list_id,
        'items': todo.items,
        'created_at': todo.created_at.isoformat()
    }


def extract_todo_item(item: TodoItem):
    return {
        'id': item.id,
        'body': item.body,
        'done': item.done,
        'todo_id': item.todo_id,
        'user_id': item.user_id,
        'created_at': item.created_at.isoformat()
    }


def todoRoutes(app: Bottle):

    @app.post('/todo/add/<list_id>')
    def add_todo_handler(db: Session, list_id):
        id = get_user_id()
        body = v.validate_body({
            'description': v.is_max_length(400)
        })

        todo = Todo(
            description=body['description'],
            list_id=list_id,
            user_id=id
        )

        db.add(todo)
        db.commit()

        return json_res(data=extract_todo(todo))

    @app.put('/todo/update/<todo_id>')
    def update_todo_handler(db: Session, todo_id):
        id = get_user_id()
        body = v.validate_body({
            'description': v.is_max_length(400)
        })

        todo = db.query(Todo).filter_by(id=todo_id, user_id=id).first()

        if todo == None:
            raise Error([system_error_item('Todo is not found.')])

        todo.description = body['description']
        db.commit()

        return json_res(data={
            'message': 'Successfully updated todo.'
        })

    @app.delete('/todo/delete/<todo_id>')
    def delete_todo_handler(db: Session, todo_id):
        id = get_user_id()

        affectedRows = db.query(Todo).filter_by(
            id=todo_id,
            user_id=id
        ).delete()

        if affectedRows == 0:
            raise Error([system_error_item('Todo is not found.')])

        return json_res(data={
            'message': 'Successfully removed todo.'
        })

    @app.post('/todo/item/add/<todo_id>')
    def add_todo_item_handler(db: Session, todo_id):
        id = get_user_id()
        body = v.validate_body({
            'body': v.is_max_length(500)
        })

        item = TodoItem(body=body['body'], user_id=id, todo_id=todo_id)

        db.add(item)
        db.commit()

        return json_res(data=extract_todo_item(item))

    @app.delete('/todo/item/delete/<item_id>')
    def delete_todo_item_handler(db: Session, item_id):
        id = get_user_id()

        affectedRows = db.query(TodoItem).filter_by(
            id=item_id,
            user_id=id
        ).delete()

        if affectedRows == 0:
            raise Error([system_error_item('Todo Item is not found.')])

        return json_res(data={
            'message': 'Successfully removed todo Item.'
        })
