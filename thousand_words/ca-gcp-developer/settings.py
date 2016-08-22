from storage import base_url, is_local
import os

BASE_URL = base_url()
WEB_CLIENT_ID = "YOU MUST GENERATE YOUR OWN IN THE CONSOLE UNDER API MANAGER > CREDENTIALS"
IS_APP_ENGINE_ENV = os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')
API_KEY = "YOU MUST GENERATE YOUR OWN IN THE CONSOLE UNDER API MANAGER > CREDENTIALS"

def init(app):
    app.debug = not IS_APP_ENGINE_ENV
    app.secret_key = 'nse8rwwn8sdh7ha7YJ234R23R237&W^%$@@#dsfdsSdu3'
