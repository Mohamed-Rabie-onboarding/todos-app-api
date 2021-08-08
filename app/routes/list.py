from utils.error import Error, system_error_item
from utils.res import json_res
from utils.jwt import get_user_id
from bottle import Bottle
from sqlalchemy.orm.session import Session
from database.models.list import List
import utils.validators as v
from routes.todo import extract_todo


def listRoutes(app: Bottle):

    def extractList(list: List):
        return {
            'id': list.id,
            'name': list.name,
            'user_id': list.user_id,
            'todos': [extract_todo(todo) for todo in list.todos]
        }

    @app.get('/list/all')
    def get_lists_handler(db: Session):
        id = get_user_id()
        lists = db.query(List).filter_by(user_id=id).all()
        return json_res(data={'lists': [extractList(list) for list in lists]})

    @app.post('/list/add')
    def add_handler(db: Session):
        id = get_user_id()
        body = v.validate_body({
            'name': v.is_min_length(1)
        })

        list = List(name=body['name'], user_id=id)

        # if something went wrong an error
        # from internal_server_error should occur by default
        db.add(list)
        db.commit()

        return json_res(data=extractList(list))

    @app.delete('/list/<list_id>')
    def delete_handler(db: Session, list_id):
        id = get_user_id()

        affectedRows = db.query(List).filter_by(
            id=list_id, user_id=id).delete()

        if affectedRows == 0:
            raise Error([system_error_item('List not found.')])

        return json_res(data={
            'message': 'Successfully remove list.'
        })

    @app.put('/list/<list_id>')
    def update_list_handler(db: Session, list_id):
        id = get_user_id()
        body = v.validate_body({
            'name': v.is_min_length(1)
        })

        list = db.query(List).filter_by(id=list_id, user_id=id).first()

        if list == None:
            raise Error([system_error_item('List is not found.')])

        list.name = body['name']
        db.commit()

        return json_res(data={'message': 'Successfully updated list.'})
