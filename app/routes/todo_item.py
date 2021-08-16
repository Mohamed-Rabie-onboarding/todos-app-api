from bottle import Bottle, request, response
from app.utils.decorators import enable_cors, required_auth
from app.utils.orm_helper import TodoItemOrmHelper
from app.utils.validator_helper import error_if_not_found
from app.database.models.todo_item import TodoItemModel
from app.routes.error import error_handler

todoItemRoutes = Bottle()
todoItemRoutes.error_handler = error_handler


@todoItemRoutes.route('/<id:int>', method=['OPTIONS', 'GET'])
@enable_cors
@required_auth
def get_item_handler(user_id: int, id: int):
    """ get_item_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 200: Item found and returned.
            - 401: Unauthorized to make this request.
            - 404: Item not found.

        :param user_id: the user `id`
        :param id: the item `id`
    """
    item = TodoItemOrmHelper.get_todo_item(id, user_id)

    error_if_not_found(item, 'TodoItem')

    response.status = 200
    return item.to_dict()


@todoItemRoutes.route('/', method=['OPTIONS', 'GET'])
@enable_cors
@required_auth
def get_items_handler(user_id: int):
    """ get_items_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 200: Items found ([] if none found) and returned.
            - 401: Unauthorized to make this request.

        :param user_id: the user `id`
    """
    response.status = 200
    return {
        'items': [
            t.to_dict() for t in TodoItemOrmHelper.get_user_todo_items(user_id)
        ]
    }


@todoItemRoutes.route('/<todo_id:int>', method=['OPTIONS', 'POST'])
@enable_cors
@required_auth
def create_todo_item_handler(user_id: int, todo_id: int):
    """ create_todo_item_handler
        required `Authorization` header with `bearer $token`
        takes in `body` includes body
        responses:
            - 201: Item created and returned.
            - 400: invalid data.
            - 401: Unauthorized to make this request.

        :param user_id: the user `id`
        :param todo_id: the todo `id`
    """
    item = TodoItemModel.factory(request.json)

    db_item = item.to_orm(user_id, todo_id)
    TodoItemOrmHelper.create_todo_item(db_item)

    response.status = 201
    return db_item.to_dict()


@todoItemRoutes.route('/<id:int>', method=['OPTIONS', 'PUT'])
@enable_cors
@required_auth
def update_todo_item_handler(user_id: int, id: int):
    """ update_todo_item_handler
        required `Authorization` header with `bearer $token`
        takes in `body` includes `Optional[body]` and `Optional[done]`
        responses:
            - 204: Item Updated and nothing to return.
            - 400: invalid data.
            - 401: Unauthorized to make this request.
            - 404: Item not found.

        :param user_id: the user `id`
        :param id: the item `id`
    """
    body = request.json
    item = TodoItemModel.factory(body, True)

    db_item = TodoItemOrmHelper.get_todo_item(id, user_id)

    error_if_not_found(db_item, 'TodoItem')

    TodoItemOrmHelper.update_todo_item(db_item, **body)
    response.status = 204


@todoItemRoutes.route('/<id:int>', method=['OPTIONS', 'DELETE'])
@enable_cors
@required_auth
def delete_todo_item_handler(user_id: int, id: int):
    """ delete_todo_item_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 204: Item Removed and nothing to return.
            - 401: Unauthorized to make this request.
            - 404: Item not found.

        :param user_id: the user `id`
        :param id: the item `id`
    """
    removed = TodoItemOrmHelper.remove_todo_item(id, user_id)

    error_if_not_found(removed, 'TodoItem')

    response.status = 204
