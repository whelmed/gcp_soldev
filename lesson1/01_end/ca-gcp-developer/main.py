import logging

from flask import (
    Flask,
)

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello from Cloud Academy"

@app.route('/greet/<name>')
def greet(name):
    return 'Hello ' + name

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error has occurred')

    return 'An error has occurred on the server', 500
