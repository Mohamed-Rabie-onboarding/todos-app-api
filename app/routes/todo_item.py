from bottle import Bottle, request, response
from utils.decorators import enable_cors, required_auth
from utils.orm_helper import TodoItemOrmHelper
from utils.validator_helper import error_if_not_found
from database.models.todo_item import TodoItemModel
from routes.error import error_handler

todoItemRoutes = Bottle()
todoItemRoutes.error_handler = error_handler


@todoItemRoutes.get('/<id:int>')
@enable_cors
@required_auth
def get_item_handler(user_id: int, id: int):
    item = TodoItemOrmHelper.get_todo_item(id, user_id)

    error_if_not_found(item, 'TodoItem')

    response.status = 200
    return item.to_dict()


@todoItemRoutes.get('/')
@enable_cors
@required_auth
def get_items_handler(user_id: int):
    response.status = 200
    return {
        'items': [
            t.to_dict() for t in TodoItemOrmHelper.get_user_todo_items(user_id)
        ]
    }


@todoItemRoutes.post('/<todo_id:int>')
@enable_cors
@required_auth
def create_todo_item_handler(user_id: int, todo_id: int):
    item = TodoItemModel.factory(request.json)

    db_item = item.to_orm(user_id, todo_id)
    TodoItemOrmHelper.create_todo_item(db_item)

    response.status = 201
    return db_item.to_dict()


@todoItemRoutes.put('/<id:int>')
@enable_cors
@required_auth
def update_todo_item_handler(user_id: int, id: int):
    body = request.json
    item = TodoItemModel.factory(body, True)

    db_item = TodoItemOrmHelper.get_todo_item(id, user_id)

    error_if_not_found(db_item, 'TodoItem')

    TodoItemOrmHelper.update_todo_item(db_item, **body)
    response.status = 204


@todoItemRoutes.delete('/<id:int>')
@enable_cors
@required_auth
def delete_todo_item_handler(user_id: int, id: int):
    removed = TodoItemOrmHelper.remove_todo_item(id, user_id)

    error_if_not_found(removed, 'TodoItem')

    response.status = 204
