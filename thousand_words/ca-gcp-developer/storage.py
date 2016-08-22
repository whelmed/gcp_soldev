import cloudstorage as gcs
from cloudstorage.common import local_api_url, local_run
from google.appengine.api import app_identity
from werkzeug.utils import secure_filename
import os

def is_local():
    return local_run()

def base_url():
    if local_run():
        return local_api_url()
    return "https://storage.googleapis.com"


BUCKET_NAME = os.environ.get('BUCKET_NAME',
                       app_identity.get_default_gcs_bucket_name())




def write(filename, content_type, content, public=True):
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    options = {}
    if public:
        options = {'x-goog-acl': 'public-read'}

    gcs_file = gcs.open(filename,
                      'w',
                      content_type=content_type,
                      options=options,
                      retry_params=write_retry_params)

    gcs_file.write(content)
    gcs_file.close()


def read_file(filename):
    gcs_file = gcs.open(filename)
    result = gcs_file.read()
    gcs_file.close()
    return result

def save_uploaded_file(uploaded_file, foldername):
    file_name = '/{0}/{1}/{2}'.format(BUCKET_NAME,
                foldername,
                secure_filename(uploaded_file.filename))
    write(file_name, uploaded_file.content_type, uploaded_file.read())
    return file_name
