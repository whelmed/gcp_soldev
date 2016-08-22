import logging

from flask import (
    Flask,
)
from google.appengine.api.modules import get_hostname
from google.appengine.ext import ndb


app = Flask(__name__)

class Greeting(ndb.Model):
    Message = ndb.StringProperty()


@app.route('/')
def index():
    return "Hello Solutions Developers - From " + get_hostname()


@app.route('/test-shared-state/<message>')
def shared_state(message):
    greeting = Greeting(Message=message)

    greeting_key = greeting.put()

    url_safe_key = greeting_key.urlsafe()

    return "Key: {0} URL Safe: {1}".format(greeting_key, url_safe_key)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error has occurred')

    return 'An error has occurred on the server', 500
