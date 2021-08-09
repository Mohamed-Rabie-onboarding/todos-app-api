from bottle import Bottle, request, response
from utils.decorators import enable_cors, required_auth
from utils.orm_helper import CollectionOrmHelper
from database.models.collection import CollectionModel
from utils.validator_helper import ValidatorHelper


collectionRoutes = Bottle()


@collectionRoutes.get('/<id:int>')
@enable_cors
@required_auth
def get_collection_handler(user_id: int, id: int):
    collection = CollectionOrmHelper.get_collection(id, user_id)

    if collection is None:
        response.status = 404
        return ValidatorHelper.create_error('Server', 'Collection not found.')

    response.status = 200
    return collection.to_dict()


@collectionRoutes.get('/')
@enable_cors
@required_auth
def get_collections_handler(user_id: int):
    response.status = 200
    return {
        'collections': [
            c.to_dict() for c in CollectionOrmHelper.get_user_collections(user_id)
        ]
    }


@collectionRoutes.post('/')
@enable_cors
@required_auth
def create_collection_handler(user_id: int):
    collection, errors = CollectionModel.factory(request.json)

    if errors is not None:
        response.status = 400
        return errors

    db_collection = collection.to_orm(user_id=user_id)
    CollectionOrmHelper.create_collection(db_collection)

    response.status = 201
    return db_collection.to_dict()


@collectionRoutes.put('/<id:int>')
@enable_cors
@required_auth
def update_collection_handler(user_id: int, id: int):
    collection, errors = CollectionModel.factory(request.json)

    if errors is not None:
        response.status = 400
        return errors

    db_collection = CollectionOrmHelper.get_collection(id, user_id)

    if db_collection is None:
        response.status = 404
        return ValidatorHelper.create_error('Server', 'Collection not found.')

    CollectionOrmHelper.update_collection(db_collection, collection.title)

    response.status = 204


@collectionRoutes.delete('/<id:int>')
@enable_cors
@required_auth
def delete_collection_handler(user_id: int, id: int):
    removed = CollectionOrmHelper.remove_collection(id, user_id)

    if not removed:
        response.status = 404
        return ValidatorHelper.create_error('Sever', 'Collection not found.')

    response.status = 204
