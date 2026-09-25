import uuid

from flask import Flask, g, request

REQUEST_ID_HEADER = "X-Request-ID"


def init_request_id(app: Flask) -> None:
    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())

    @app.after_request
    def add_request_id_header(response):
        response.headers[REQUEST_ID_HEADER] = g.request_id
        return response
