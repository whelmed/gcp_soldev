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

from models import Category, Image, SiteMetadata
from settings import init, IS_APP_ENGINE_ENV
from google.appengine.api.modules import get_hostname
from postfile import post_file

app = Flask(__name__)

# apply our settings
init(app)

@app.route('/init/')
def index():
    ''' If this fails with: IOError: [Errno 13] file not accessible:
        Comment out the section in the app.yaml
        - url: /static
          static_dir: static

        and try again.
    '''
    meta = SiteMetadata.get()

    if meta.initialized:
        return "Already done. See metadata"

    uploads = {
        "Automobiles": {
            "car.jpg": "I want!",
        },
        "Sports": {
            "sports.jpeg": "So cool",
        },
        "Art": {
            "art.jpg": "Water colors FTW!",
        },
        "Technology": {
            "mac.jpg": "Upgrade time",
        },
        "Nature": {
            "flower.jpeg": "Pretty",
            "marigold.jpeg": "Great pic",
        },
        "Science": {
            "science.jpg": ":O",
            "sci2.jpg": "This is great!",
        },
        "Animals": {
            "lion.jpeg": "Yikes",
            "puppy.jpeg": "Awww",
            "puppy2.jpeg": "Cute!",
        },
        "Fire": {
            "fire.jpeg": "Neat"
        },
        "Games": {
            "game.jpeg": "Game on!"
        },
        "Education": {
            "edu.jpg": "If I only had a brain",
            "edu2.jpg": "So smart",
        },
        "Toys": {
            "toys.jpg": "Play time"
        },
        "Food": {
            "veggies.jpeg": "Yum",
            "veggies.jpg": "Food!",
        },
    }

    hostname = get_hostname()
    url = "http://{0}/{1}".format(hostname, "images/new/")
    base_dir = ''

    if IS_APP_ENGINE_ENV:
        url = "https://{0}/{1}".format(hostname, "images/new/")
        base_dir = os.path.dirname(os.path.realpath(__file__))

    for category in uploads:
        cat = Category.by_name(category) or Category(name=category)
        cat.put()

        for image in uploads[category]:
            fpath = os.path.join(base_dir, 'static/init/', image)
            f = open(fpath, 'rb')
            size = os.stat(fpath).st_size

            data = {
                'cat_id': cat.key.urlsafe(),
                'details': uploads[category][image]
            }

            post_file(url, image, "image/jpeg", size, f, data)

    meta.initialized = True
    meta.put()

    return "Complete"


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error has occurred')

    return 'An error has occurred on the server', 500
