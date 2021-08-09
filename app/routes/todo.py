from bottle import Bottle, request, response
from utils.decorators import enable_cors, required_auth
from database.models.todo import TodoModel
from utils.orm_helper import TodoOrmHelper, CollectionOrmHelper
from utils.validator_helper import ValidatorHelper

todoRoutes = Bottle()


@todoRoutes.get('/<id:int>')
@enable_cors
@required_auth
def get_todo_handler(user_id: int, id: int):
    todo = TodoOrmHelper.get_todo(id, user_id)

    if todo is None:
        response.status = 404
        return ValidatorHelper.create_error('Server', 'Todo not found.')

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


@todoRoutes.get('/<collection_id:int>')
@enable_cors
@required_auth
def get_collection_todos_handler(user_id: int, collection_id: int):
    collection = CollectionOrmHelper.get_collection(collection_id, user_id)

    if collection is None:
        response.status = 404
        return ValidatorHelper.create_error('Sever', 'Collection not found.')

    response.status = 200
    return {
        'todos': [
            t.to_dict() for t in collection.todos
        ]
    }


@todoRoutes.post('/<collection_id:int>')
@enable_cors
@required_auth
def create_todo_handler(user_id: int, collection_id: int):
    todo, errors = TodoModel.factory(request.json)

    if errors is not None:
        response.status = 400
        return errors

    db_todo = todo.to_orm(user_id=user_id, collection_id=collection_id)
    TodoOrmHelper.create_todo(db_todo)

    response.status = 201


@todoRoutes.put('/<id:int>')
@enable_cors
@required_auth
def update_todo_handler(user_id: int, id: int):
    todo, errors = TodoModel.factory(request.json)

    if errors is not None:
        response.status = 400
        return errors

    db_todo = TodoOrmHelper.get_todo(id, user_id)

    if db_todo is None:
        response.status = 404
        return ValidatorHelper.create_error('Sever', 'Todo not found.')

    TodoOrmHelper.update_todo(db_todo, todo.description)

    response.status = 204


@todoRoutes.delete('/<id:int>')
@enable_cors
@required_auth
def delete_todo_handler(user_id: int, id: int):
    removed = TodoOrmHelper.remove_todo(id, user_id)

    if not removed:
        response.status = 404
        return ValidatorHelper.create_error('Sever', 'Todo not found.')

    response.status = 204
