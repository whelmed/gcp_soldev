import logging
import os
import json
import httplib2

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from oauth2client import client
from apiclient.discovery import build
from settings import init

app = Flask(__name__)

# apply our settings
init(app)

@app.route('/from-drive/')
def from_drive():
    return render_template('from_drive.html', context={})

@app.route('/from-drive/files/')
def from_drive_files():
    if 'credentials' not in session:
        return redirect(url_for('oauth2callback'))

    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect(url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = build('drive', 'v3', http=http_auth)
        files = drive_service.files().list().execute()

        return render_template('from_drive.html', context={ "files": files['files'] })
    return render_template('from_drive.html')


@app.route('/from-drive/oauth2callback')
def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
      redirect_uri=url_for('oauth2callback', _external=True))

  flow.params['include_granted_scopes'] = "true"

  if 'code' not in request.args:
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)
  else:
    auth_code = request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    session['credentials'] = credentials.to_json()
    return redirect(url_for('from_drive'))



@app.errorhandler(500)
def server_error(e):
    logging.exception('An error has occurred')

    return 'An error has occurred on the server', 500
