from bottle import Bottle
from utils.getBody import get_body
import utils.validators as v
from utils.res import json_res
from sqlalchemy.orm.session import Session


def listRoutes(app: Bottle):

    @app.get('/list/all')
    def get_lists_handler(db: Session):
        return 'get_lists_handler'

    @app.post('/list/add')
    def add_handler(db: Session):
        return 'list added'

    @app.delete('/list/<id>')
    def delete_handler(db: Session, id):
        return 'list deleted'

    @app.put('/list/<id>')
    def update_list_handler(db: Session):
        return 'update list handler'
