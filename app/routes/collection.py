from bottle import Bottle, request, response
from utils.decorators import enable_cors, required_auth
from utils.orm_helper import CollectionOrmHelper
from database.models.collection import CollectionModel
from utils.validator_helper import error_if_not_found
from routes.error import error_handler

collectionRoutes = Bottle()
collectionRoutes.error_handler = error_handler


@collectionRoutes.get('/<id:int>')
@enable_cors
@required_auth
def get_collection_handler(user_id: int, id: int):
    """ get_collection_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 204: todo updated and nothing to return.
            - 401: Unauthorized to make this request.
            - 404: Collection not found.

        :param user_id: the user `id`
        :param id: the collection `id`
    """
    collection = CollectionOrmHelper.get_collection(id, user_id)

    error_if_not_found(collection, 'Collection')

    response.status = 200
    return collection.to_dict()


@collectionRoutes.get('/')
@enable_cors
@required_auth
def get_collections_handler(user_id: int):
    """ get_collection_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 200: collections return.
            - 401: Unauthorized to make this request.

        :param user_id: the user `id`
        :param id: the collection `id`
    """
    response.status = 200
    return {
        'collections': [
            c.to_dict() for c in CollectionOrmHelper.get_user_collections(user_id)
        ]
    }


@collectionRoutes.get('/<id:int>/todos')
@enable_cors
@required_auth
def get_collection_todos_handler(user_id: int, id: int):
    """ get_collection_todos_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 200: todos returned.
            - 401: Unauthorized to make this request.
            - 404: Collection not found.

        :param user_id: the user `id`
        :param id: the collection `id`
    """
    collection = CollectionOrmHelper.get_collection(id, user_id)

    error_if_not_found(collection, 'Collection')

    response.status = 200
    return {
        'todos': [
            t.to_dict() for t in collection.todos
        ]
    }


@collectionRoutes.get('/<id:int>/items')
@enable_cors
@required_auth
def get_collection_items_handler(user_id: int, id: int):
    """ get_collection_items_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 200: items returned.
            - 401: Unauthorized to make this request.
            - 404: Collection not found.

        :param user_id: the user `id`
        :param id: the collection `id`
    """
    collection = CollectionOrmHelper.get_collection(id, user_id)

    error_if_not_found(collection, 'Collection')

    response.status = 200

    items = []
    for todo in collection.todos:
        for item in todo.items:
            items.append(item.to_dict())

    # for loop more readable
    # [item for item in (todo.items for todo in collection.todos)]

    return {
        'items': items
    }


@collectionRoutes.post('/')
@enable_cors
@required_auth
def create_collection_handler(user_id: int):
    """ create_collection_handler
        required `Authorization` header with `bearer $token`
        takes in `body` includes title
        responses:
            - 201: collection created and returned.
            - 400: invalid data.
            - 401: Unauthorized to make this request.

        :param user_id: the user `id`
    """
    collection = CollectionModel.factory(request.json)

    db_collection = collection.to_orm(user_id=user_id)
    CollectionOrmHelper.create_collection(db_collection)

    response.status = 201
    return db_collection.to_dict()


@collectionRoutes.put('/<id:int>')
@enable_cors
@required_auth
def update_collection_handler(user_id: int, id: int):
    """ update_collection_handler
        required `Authorization` header with `bearer $token`
        takes in `body` includes title
        responses:
            - 201: collection created and returned.
            - 400: invalid data.
            - 401: Unauthorized to make this request.
            - 404: Collection not found.

        :param user_id: the user `id`
        :param id: the collection `id`
    """
    collection = CollectionModel.factory(request.json)

    db_collection = CollectionOrmHelper.get_collection(id, user_id)

    error_if_not_found(db_collection, 'Collection')

    CollectionOrmHelper.update_collection(db_collection, collection.title)
    response.status = 204


@collectionRoutes.delete('/<id:int>')
@enable_cors
@required_auth
def delete_collection_handler(user_id: int, id: int):
    """ delete_collection_handler
        required `Authorization` header with `bearer $token`
        responses:
            - 201: collection created and returned.
            - 401: Unauthorized to make this request.
            - 404: Collection not found.

        :param user_id: the user `id`
        :param id: the collection `id`
    """
    removed = CollectionOrmHelper.remove_collection(id, user_id)

    error_if_not_found(removed, 'Collection')

    response.status = 204
