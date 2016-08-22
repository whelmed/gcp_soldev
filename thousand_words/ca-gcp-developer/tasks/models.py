from google.appengine.ext import ndb


class Image(ndb.Model):
    '''Models an individual image'''
    url = ndb.StringProperty()
    details = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)
    created_on = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def key_for_url_string(cls, url_string):
        '''Fetch a key base on the URL safe key.'''
        return ndb.Key(urlsafe=url_string)

    @classmethod
    def entity_for_urlsafe_key(cls, url_string):
        return cls.key_for_url_string(url_string).get()
