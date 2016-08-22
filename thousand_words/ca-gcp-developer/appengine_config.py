# https://github.com/GoogleCloudPlatform/gcloud-python/issues/2032
# This is a monkey patch to fix an issue with App Engine that
# hasn't been fixed yet in production.
import os.path

def patched_expanduser(path):
    return path

os.path.expanduser = patched_expanduser

# Import the vendor libraries.
from google.appengine.ext import vendor

vendor.add('lib')
