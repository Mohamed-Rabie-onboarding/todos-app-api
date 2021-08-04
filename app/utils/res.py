import json
from bottle import response


def json_res(*_, data=None, errors=None):
    response.set_header('Content-Type', 'application/json')
    return json.dumps({
        'success': data is not None,
        'data': data,
        'errors': errors
    })
