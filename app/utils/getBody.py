from bottle import request
from json import loads


def get_body():
    bytes = request.body
    values = bytes.getvalue()
    body = values.decode('utf-8')
    return loads(body)
