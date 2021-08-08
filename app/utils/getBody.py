from bottle import request
from json import loads


def get_body():
    # request.json
    bytes = request.body
    values = bytes.getvalue()
    body = values.decode('utf-8')
    return loads(body)
