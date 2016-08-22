import logging
import os
import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from models import Category, Image, SiteMetadata
from settings import init, BASE_URL
from storage import save_uploaded_file
from google.appengine.api import users
from google.appengine.api import taskqueue

app = Flask(__name__)

# apply our settings
init(app)

@app.route('/images/new/', methods=['POST', 'GET'])
def create_image():
    '''Create an image'''
    logging.info('Attempting to upload new file')
    context = {
        'categories': Category.names(),
        'metadata': SiteMetadata.get()
    }

    if request.method == 'GET':
        return render_template('create_image.html', context=context)

    cat_id      = request.form['cat_id']
    category    = Category.entity_for_urlsafe_key(cat_id)
    upload      = request.files['file']
    details     = request.form['details']
    upload      = request.files['file']

    # The app.yaml file ensures that users are logged in before
    # making it to this page.
    user    = users.get_current_user()
    folder  = "public"

    if user:
        folder = user.user_id()

    # Saves the file and returns the name, minus the base URL.
    saved_file_name = save_uploaded_file(upload, folder)
    # Create the image
    img = Image(parent=category.key, url=saved_file_name, details=details)

    # And save it.
    key = img.put()


    payload = json.dumps({'bucketname': saved_file_name, 'key': key.urlsafe() })
    # target is the service we want to send this to.
    taskqueue.add(url='/tasks/apply-tags/', payload=payload, target='tasks')

    # Notify the user
    flash('Upload Complete')

    return redirect(url_for('create_image'))


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error has occurred')

    return 'An error has occurred on the server', 500
