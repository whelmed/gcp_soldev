import logging
import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

from models import Category, Image, SiteMetadata
from settings import init, BASE_URL, API_KEY
from oauth2client import client
from apiclient.discovery import build
app = Flask(__name__)

# apply our settings
init(app)

@app.route('/images/categories/<slug>')
def categories(slug):
    '''Show all images for a given category '''
    context = {'images': Image.for_category(Category.key_for_url_string(slug)),
               'base_url': BASE_URL,
               'image_count': Image.image_count()
    }

    return render_template('category.html', context=context)

@app.route('/images/<slug>/')
def image(slug):
    ''' Show a single image give the safe url key passed in via the URL '''
    context = {'image': Image.entity_for_urlsafe_key(slug),
               'base_url': BASE_URL,
               'metadata': SiteMetadata.get()
    }

    return render_template('image.html', context=context)


@app.route('/images/short-url/')
def short_url():
    ''' returns a shortened URL. '''
    urlshortener = build('urlshortener', 'v1', developerKey=API_KEY)
    root_url = request.url_root
    url_to_shorten = request.args.get('url')

    if not url_to_shorten:
        return "Invalid param", 500

    if not url_to_shorten.startswith(root_url):
        return "Invalid url", 500

    obj = urlshortener.url().insert(body={ 'longUrl': url_to_shorten }).execute()


    return jsonify(obj)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error has occurred')

    return 'An error has occurred on the server', 500
