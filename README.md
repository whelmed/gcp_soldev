# Cloud Academy

## Developing Solutions for Google Cloud Platform

### This is a demo application that runs on App Engine. It's used to accompany the [course](https://cloudacademy.com/google/developing-solutions-for-google-cloud-platform-course/)

The libraries are included, however, its probably best to clear out the lib folder and install with pip from the requirements.txt

> ` > pip install -t lib -r requirements.txt`

In order to set up the application you'll need to initialize it.
You can do this by calling the /init/ URL.

First, comment out line 36 in the app.yaml.
    - url: /images/new/
      script: upload.app
      #login: required


If this fails with: IOError: [Errno 13] file not accessible:

Comment out the section in the app.yaml and try again.
    #- url:  /static
    #    static_dir: static


Once it has been initialized, you can uncomment these out. It's not a perfect method of initialization, however it only happens once.

Also, you'll need to generate an OAuth2 key in the Console. Save it under the thousand_words/ca-gcp-developer/ directory named client_secrets.json

And create a key for the App Engine default service account. Save it in the same folder as above and name it service_account.json

And finally, create a Simple API key in the console (API Manager > Credentials).

You'll need to add the simple API key to the settings.py file, and the WEB_CLIENT_ID as well.
