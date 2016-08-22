# Based on Google's demo code found at:
# https://github.com/GoogleCloudPlatform/cloud-vision/blob/master/python/label/label.py
import base64
import httplib2
import os
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

IS_APP_ENGINE_ENV = os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')
# The url template to retrieve the discovery document for trusted testers.
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


def get_tags_from_image(bucket):
    if not IS_APP_ENGINE_ENV:
        return []

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_URL)

    # clean up the bucket name
    if bucket and bucket.startswith('/'):
        bucket = bucket[1:]

    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'source': {
                    "gcsImageUri": "gs://{0}".format(bucket)
                }
            },
            'features': [{
                'type': 'LABEL_DETECTION',
                'maxResults': 10
            }]
        }]
    })

    response = service_request.execute()
    print response
    return [obj['description'] for obj in response['responses'][0]['labelAnnotations']]
