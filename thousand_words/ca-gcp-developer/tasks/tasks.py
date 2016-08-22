import logging
import json
import os
from flask import (
    Flask,
    request,
)

from models import Image
from googleapiclient.errors import HttpError
from parseimage import get_tags_from_image
from google.appengine.api import mail

app = Flask(__name__)



@app.route('/tasks/apply-tags/', methods=["POST"])
def index():
    logging.info('attempting to apply tags')

    data = json.loads(request.get_data())

    image_url_safe_key = data.get('key')
    bucket_name = data.get('bucketname')
    # Attempt to tag the image via the image API.
    try:
        img = Image.entity_for_urlsafe_key(image_url_safe_key)
        img.tags = get_tags_from_image(bucket_name)
        img.put()
    except HttpError as e:
        if 'it is disabled' in e:
            logging.error('Vision API is not enabled')

    return "Success!", 200


@app.route('/tasks/email-user/')
def mailer():
    message = mail.EmailMessage(
        sender='ben@ca-gcp-developer.appspotmail.com',
        subject="Cron is working.")

    message.to = "Ben Lambert <ben.lambert@cloudacademy.com>"
    message.body = "This is a regular email. Cool, eh?"
    message.send()
    return "Success!", 200


@app.route('/')
def test():
    return "Success!", 200


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
