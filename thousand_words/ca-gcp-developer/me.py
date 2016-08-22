import logging
import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from models import Category, Image
from settings import init, BASE_URL
from google.appengine.api import users

app = Flask(__name__)

# apply our settings
init(app)

@app.route('/me/')
def me():
    '''Returns the profile page'''

    context = {
        'user':     users.get_current_user(),
        'logout':   users.create_logout_url('/'),
        'is_admin': users.is_current_user_admin(),
    }
    logging.info("Current user: {}".format(context['user']))

    return render_template('me.html', context=context)




@app.errorhandler(500)
def server_error(e):
    logging.exception('An error has occurred')

    return 'An error has occurred on the server', 500
