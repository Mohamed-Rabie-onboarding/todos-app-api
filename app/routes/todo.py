from bottle import Bottle, request, response
from app.utils.decorators import enable_cors, required_auth
from app.database.models.todo import TodoModel
from app.utils.orm_helper import TodoOrmHelper
from app.utils.validator_helper import error_if_not_found
from app.routes.error import error_handler

todoRoutes = Bottle()
todoRoutes.error_handler = error_handler


@todoRoutes.route('/<id:int>', method=['OPTIONS', 'GET'])
@enable_cors
@required_auth
def get_todo_handler(user_id: int, id: int):
    """ get_todo_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 200: Todo found and returned.
            - 401: Unauthorized to make this request.
            - 404: todo not found.

        :param user_id: the user `id`
        :param id: the todo `id`
    """
    todo = TodoOrmHelper.get_todo(id, user_id)

    error_if_not_found(todo, 'Todo')

    response.status = 200
    return todo.to_dict()


@todoRoutes.route('/', method=['OPTIONS', 'GET'])
@enable_cors
@required_auth
def get_todos_handler(user_id: int):
    """ get_todos_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 200: Todos returned.
            - 401: Unauthorized to make this request.

        :param user_id: the user `id`
    """
    response.status = 200
    return {
        'todos': [
            t.to_dict() for t in TodoOrmHelper.get_user_todos(user_id)
        ]
    }


@todoRoutes.route('/<id:int>/items', method=['OPTIONS', 'GET'])
@enable_cors
@required_auth
def get_todo_items_handler(user_id: int, id: int):
    """ get_todo_items_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 200: items returned.
            - 401: Unauthorized to make this request.
            - 404: Todo not found.

        :param user_id: the user `id`
        :param id: the todo `id`
    """
    todo = TodoOrmHelper.get_todo(id, user_id)

    error_if_not_found(todo, 'Todo')

    response.status = 200
    return {
        'items': [
            item.to_dict() for item in todo.items
        ]
    }


@todoRoutes.route('/<collection_id:int>', method=['OPTIONS', 'POST'])
@enable_cors
@required_auth
def create_todo_handler(user_id: int, collection_id: int):
    """ create_todo_handler
        required `Authorization` header with `bearer $token`
        takes in `body` includes description
        responses:
            - 201: todo created and returned.
            - 400: invalid data.
            - 401: Unauthorized to make this request.

        :param user_id: the user `id`
        :param collection_id: the collection `id`
    """
    todo = TodoModel.factory(request.json)

    db_todo = todo.to_orm(user_id=user_id, collection_id=collection_id)
    TodoOrmHelper.create_todo(db_todo)

    response.status = 201
    return db_todo.to_dict()


@todoRoutes.route('/<id:int>', method=['OPTIONS', 'PUT'])
@enable_cors
@required_auth
def update_todo_handler(user_id: int, id: int):
    """ update_todo_handler
        required `Authorization` header with `bearer $token`
        takes in `body` includes description
        responses:
            - 204: todo updated and nothing to return.
            - 400: invalid data.
            - 401: Unauthorized to make this request.

        :param user_id: the user `id`
        :param id: the todo `id`
    """
    todo = TodoModel.factory(request.json)

    db_todo = TodoOrmHelper.get_todo(id, user_id)

    error_if_not_found(db_todo, 'Todo')

    TodoOrmHelper.update_todo(db_todo, todo.description)

    response.status = 204


@todoRoutes.route('/<id:int>', method=['OPTIONS', 'DELETE'])
@enable_cors
@required_auth
def delete_todo_handler(user_id: int, id: int):
    """ delete_todo_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 204: todo removed and nothing to return.
            - 401: Unauthorized to make this request.
            - 404: Todo not found

        :param user_id: the user `id`
        :param id: the todo `id`
    """
    removed = TodoOrmHelper.remove_todo(id, user_id)

    error_if_not_found(removed, 'Todo')

    response.status = 204
