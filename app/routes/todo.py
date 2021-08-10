from bottle import Bottle, request, response
from utils.decorators import enable_cors, required_auth
from database.models.todo import TodoModel
from utils.orm_helper import TodoOrmHelper
from utils.validator_helper import error_if_not_found
from routes.error import error_handler

todoRoutes = Bottle()
todoRoutes.error_handler = error_handler


@todoRoutes.get('/<id:int>')
@enable_cors
@required_auth
def get_todo_handler(user_id: int, id: int):
    todo = TodoOrmHelper.get_todo(id, user_id)

    error_if_not_found(todo, 'Todo')

    response.status = 200
    return todo.to_dict()


@todoRoutes.get('/')
@enable_cors
@required_auth
def get_todos_handler(user_id: int):
    response.status = 200
    return {
        'todos': [
            t.to_dict() for t in TodoOrmHelper.get_user_todos(user_id)
        ]
    }


@todoRoutes.get('/<id:int>/items')
@enable_cors
@required_auth
def get_todo_items_handler(user_id: int, id: int):
    todo = TodoOrmHelper.get_todo(id, user_id)

    error_if_not_found(todo, 'Todo')

    response.status = 200
    return {
        'items': [
            item.to_dict() for item in todo.items
        ]
    }


@todoRoutes.post('/<collection_id:int>')
@enable_cors
@required_auth
def create_todo_handler(user_id: int, collection_id: int):
    todo = TodoModel.factory(request.json)

    db_todo = todo.to_orm(user_id=user_id, collection_id=collection_id)
    TodoOrmHelper.create_todo(db_todo)

    response.status = 201
    return db_todo.to_dict()


@todoRoutes.put('/<id:int>')
@enable_cors
@required_auth
def update_todo_handler(user_id: int, id: int):
    todo = TodoModel.factory(request.json)

    db_todo = TodoOrmHelper.get_todo(id, user_id)

    error_if_not_found(db_todo, 'Todo')

    TodoOrmHelper.update_todo(db_todo, todo.description)

    response.status = 204


@todoRoutes.delete('/<id:int>')
@enable_cors
@required_auth
def delete_todo_handler(user_id: int, id: int):
    removed = TodoOrmHelper.remove_todo(id, user_id)

    error_if_not_found(removed, 'Todo')

    response.status = 204
