import logging

from flask import (
    Flask,
)

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello Solutions Developers"

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error has occurred')

    return 'An error has occurred on the server', 500
