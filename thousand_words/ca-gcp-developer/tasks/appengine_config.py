# https://github.com/GoogleCloudPlatform/gcloud-python/issues/2032
import os.path

def patched_expanduser(path):
    return path

os.path.expanduser = patched_expanduser

from google.appengine.ext import vendor

vendor.add('lib')
