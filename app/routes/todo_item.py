from bottle import Bottle, request, response
from utils.decorators import enable_cors, required_auth
from database.models.todo import TodoModel
from utils.orm_helper import TodoItemOrmHelper, TodoOrmHelper, CollectionOrmHelper
from utils.validator_helper import ValidatorHelper
from database.models.todo_item import TodoItemModel

todoItemRoutes = Bottle()


@todoItemRoutes.get('/<id:int>')
@enable_cors
@required_auth
def get_item_handler(user_id: int, id: int):
    item = TodoItemOrmHelper.get_todo_item(id, user_id)

    if item is None:
        response.status = 404
        return ValidatorHelper.create_error('Server', 'TodoItem not found.')

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


@todoItemRoutes.get('/<todo_id:int>')
@enable_cors
@required_auth
def get_todo_items_handler(user_id: int, todo_id: int):
    todo = TodoOrmHelper.get_todo(todo_id, user_id)

    if todo is None:
        response.status = 404
        return ValidatorHelper.create_error('Sever', 'Todo not found.')

    response.status = 200
    return {
        'items': [
            item.to_dict() for item in todo.items
        ]
    }


@todoItemRoutes.get('/<collection_id:int>')
@enable_cors
@required_auth
def get_collection_items_handler(user_id: int, collection_id: int):
    collection = CollectionOrmHelper.get_collection(collection_id, user_id)

    if collection is None:
        response.status = 404
        return ValidatorHelper.create_error('Sever', 'Collection not found.')

    response.status = 200

    items = []
    for todo in collection.todos:
        for item in todo.items:
            items.append(item)

    # for loop more readable
    # [item for item in (todo.items for todo in collection.todos)]

    return {
        'items': items
    }


@todoItemRoutes.post('/<todo_id:int>')
@enable_cors
@required_auth
def create_todo_item_handler(user_id: int, todo_id: int):
    item, errors = TodoItemModel.factory(request.json)

    if errors is not None:
        response.status = 400
        return errors

    db_item = item.to_orm(user_id, todo_id)
    TodoItemOrmHelper.create_todo_item(db_item)

    response.status = 201


@todoItemRoutes.put('/<id:int>')
@enable_cors
@required_auth
def update_todo_item_handler(user_id: int, id: int):
    body = request.json
    item, errors = TodoItemModel.factory(body, True)

    if errors is not None:
        response.status = 400
        return errors

    db_item = TodoItemOrmHelper.get_todo_item(id, user_id)

    if db_item is None:
        response.status = 404
        return ValidatorHelper.create_error('Sever', 'TodoItem not found.')

    TodoItemOrmHelper.update_todo_item(db_item, **body)

    response.status = 204


@todoItemRoutes.delete('/<id:int>')
@enable_cors
@required_auth
def delete_todo_item_handler(user_id: int, id: int):
    removed = TodoItemOrmHelper.remove_todo_item(id, user_id)

    if not removed:
        response.status = 404
        return ValidatorHelper.create_error('Sever', 'TodoItem not found.')

    response.status = 204
