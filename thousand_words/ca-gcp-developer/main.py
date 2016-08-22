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
from settings import init, BASE_URL

app = Flask(__name__)

# apply our settings
init(app)

@app.route('/')
def index():
    logging.info('index page being loaded')
    context = { 'categories': {},
                'image_count': Image.image_count()
    }

    data = Category.last_image_for_n_categories()

    logging.info('categories are being loaded')
    for category, img in data:
        logging.info('Fetching images for {}'.format(category.name))

        # If there's no image, we don't care about this category
        if img is None:
            logging.info('{} has no images'.format(category.name))
            continue

        ''' Set up the context.
            It'll end up being something like:
            "context": {
                "metadata": {...} # see SiteMetadata
                "categories": {
                    "Art": {
                        "url":      "http://example.com/file.jpg",
                        "count":    1
                        "slug":     "asad8ad8ad3e328nnksdsdfsdfwewe4d"
                    },
                    "Nature": {
                        "url":      "http://example.com/nature.jpg",
                        "count":    1
                        "slug":     "73sdnduubdjfndkopwiijwu3bf-ddw3"
                    }
                }
            }
        '''
        context['categories'][category.name] = {
            'url': '{0}{1}'.format(BASE_URL, img.url or ''),
            'count': Image.count_for_category(category.key),
            'slug': category.key.urlsafe()
        }
        logging.info("Rendering template for index.html")
    return render_template('index.html', context=context)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error has occurred')

    return 'An error has occurred on the server', 500
