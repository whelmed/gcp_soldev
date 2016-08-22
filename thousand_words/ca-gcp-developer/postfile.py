''' Code snippet from: http://stackoverflow.com/questions/21101854/gae-urlfetch-multipart-post-not-working-with-large-files
'''
import base64
import json
import logging
from poster.encode import multipart_encode, MultipartParam
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60)

def post_file(url, file_name, file_type, file_size, file_obj, options=dict(), username=None, password=None):

    # Input checks
    if url is None:
        raise ValueError('url')

    if file_name is None:
        raise ValueError('file_name')

    if file_type is None:
        raise ValueError('file_type')

    if file_size is None:
        raise ValueError('file_size')

    if file_obj is None:
        raise ValueError('file_obj')

    if options is None:
        raise ValueError('options')

    logging.debug('Preparing file {0}'.format(file_name))

    # This is the post arguments section
    options['file'] = MultipartParam('file', filename=file_name, filetype=file_type, filesize=file_size, fileobj=file_obj)

    data, headers = multipart_encode(options)

    logging.debug('Submitting the file to {0}'.format(url))

    # For authorization (optional)
    if username is not None and password is not None:
        headers['Authorization'] = generate_authorization_header(username, password)

    fetch = urlfetch.fetch(url=url, payload="".join(data), method=urlfetch.POST, headers=headers)
    response = fetch.content

    return response
