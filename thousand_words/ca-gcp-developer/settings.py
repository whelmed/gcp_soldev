from storage import base_url, is_local
import os

BASE_URL = base_url()
WEB_CLIENT_ID = "456059600599-5fn123oea6620987leoeq3nqfl84prah.apps.googleusercontent.com"
IS_APP_ENGINE_ENV = os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')
API_KEY = "AIzaSyD-XxybALWOqkine21u0Ry_h3HeQWGpbQ8"

def init(app):
    app.debug = not IS_APP_ENGINE_ENV
    app.secret_key = 'nse8rwwn8sdh7ha7YJ234R23R237&W^%$@@#dsfdsSdu3'
